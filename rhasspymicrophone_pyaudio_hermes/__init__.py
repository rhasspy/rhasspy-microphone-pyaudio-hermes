"""Hermes MQTT server for Rhasspy TTS using external program"""
import audioop
import io
import logging
import threading
import typing
import wave

import pyaudio
from rhasspyhermes.audioserver import AudioFrame

_LOGGER = logging.getLogger(__name__)


class MicrophoneHermesMqtt:
    """Hermes MQTT server for Rhasspy microphone input using external program."""

    def __init__(
        self,
        client,
        sample_rate: int,
        sample_width: int,
        channels: int,
        device_index: typing.Optional[int] = None,
        chunk_size: int = 2048,
        siteId: str = "default",
    ):
        self.client = client
        self.sample_rate = sample_rate
        self.sample_width = sample_width
        self.channels = channels
        self.device_index = device_index
        self.frames_per_buffer = chunk_size // sample_width
        self.siteId = siteId

        self.audioframe_topic: str = AudioFrame.topic(siteId=self.siteId)

    # -------------------------------------------------------------------------

    def record(self):
        """Record audio from PyAudio device."""
        try:
            audio = pyaudio.PyAudio()

            # Open device
            mic = audio.open(
                input_device_index=self.device_index,
                channels=self.channels,
                format=audio.get_format_from_width(self.sample_width),
                rate=self.sample_rate,
                input=True,
            )

            assert mic is not None
            mic.start_stream()
            _LOGGER.debug("Recording audio")

            try:
                # Read frames and publish as MQTT WAV chunks
                while True:
                    chunk = mic.read(self.frames_per_buffer)
                    if chunk:
                        with io.BytesIO() as wav_buffer:
                            wav_file: wave.Wave_write = wave.open(wav_buffer, "wb")
                            with wav_file:
                                wav_file.setframerate(self.sample_rate)
                                wav_file.setsampwidth(self.sample_width)
                                wav_file.setnchannels(self.channels)
                                wav_file.writeframes(chunk)

                            # Publish to audioFrame topic
                            self.client.publish(
                                self.audioframe_topic, wav_buffer.getvalue()
                            )
            finally:
                mic.stop_stream()
                audio.terminate()

        except Exception:
            _LOGGER.exception("record")

    # -------------------------------------------------------------------------

    def on_connect(self, client, userdata, flags, rc):
        """Connected to MQTT broker."""
        try:
            threading.Thread(target=self.record, daemon=True).start()
        except Exception:
            _LOGGER.exception("on_connect")

    # -------------------------------------------------------------------------

    @classmethod
    def test_microphones(
        cls,
        sample_rate: int,
        sample_width: int,
        channels: int,
        audio: typing.Optional[pyaudio.PyAudio] = None,
        chunk_size: int = 2048,
    ) -> typing.Dict[int, str]:
        """Tests available microhones and returns results"""
        # Thanks to the speech_recognition library!
        # https://github.com/Uberi/speech_recognition/blob/master/speech_recognition/__init__.py
        result = {}
        audio = audio or pyaudio.PyAudio()
        try:
            default_name = audio.get_default_input_device_info().get("name")
            for device_index in range(audio.get_device_count()):
                device_info = audio.get_device_info_by_index(device_index)
                device_name = device_info.get("name")
                if device_name == default_name:
                    device_name += "*"

                try:
                    _LOGGER.debug(
                        "Testing %s (%s) with (rate=%s, width=%s, chananels=%s)",
                        device_name,
                        device_index,
                        sample_rate,
                        sample_width,
                        channels,
                    )

                    # read audio
                    pyaudio_stream = audio.open(
                        input_device_index=device_index,
                        channels=channels,
                        format=audio.get_format_from_width(sample_width),
                        rate=sample_rate,
                        input=True,
                    )
                    try:
                        buffer = pyaudio_stream.read(chunk_size)
                        if not pyaudio_stream.is_stopped():
                            pyaudio_stream.stop_stream()
                    finally:
                        pyaudio_stream.close()
                except Exception:
                    result[device_index] = f"{device_name} (error)"
                    continue

                # compute RMS of debiased audio
                energy = -audioop.rms(buffer, 2)
                energy_bytes = bytes([energy & 0xFF, (energy >> 8) & 0xFF])
                debiased_energy = audioop.rms(
                    audioop.add(buffer, energy_bytes * (len(buffer) // 2), 2), 2
                )

                if debiased_energy > 30:  # probably actually audio
                    result[device_index] = f"{device_name} (working!)"
                else:
                    result[device_index] = f"{device_name} (no sound)"
        finally:
            audio.terminate()

        return result
