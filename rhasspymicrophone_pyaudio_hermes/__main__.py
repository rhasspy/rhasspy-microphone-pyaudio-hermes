"""Hermes MQTT service for Rhasspy TTS with PyAudio."""
import argparse
import asyncio
import logging
import sys

import paho.mqtt.client as mqtt
import rhasspyhermes.cli as hermes_cli

from . import MicrophoneHermesMqtt

_LOGGER = logging.getLogger("rhasspymicrophone_pyaudio_hermes")


def main():
    """Main method."""
    parser = argparse.ArgumentParser(prog="rhasspy-microphone-pyaudio-hermes")
    parser.add_argument(
        "--list-devices", action="store_true", help="List available input devices"
    )
    parser.add_argument("--device-index", type=int, help="Index of microphone to use")
    parser.add_argument(
        "--sample-rate",
        type=int,
        help="Sample rate of recorded audio in hertz (e.g., 16000)",
    )
    parser.add_argument(
        "--sample-width",
        type=int,
        help="Sample width of recorded audio in bytes (e.g., 2)",
    )
    parser.add_argument(
        "--channels", type=int, help="Number of channels in recorded audio (e.g., 1)"
    )
    parser.add_argument(
        "--output-site-id", help="If set, output audio data to a different site id"
    )
    parser.add_argument(
        "--udp-audio-host",
        default="127.0.0.1",
        help="Host for UDP audio (default: 127.0.0.1)",
    )
    parser.add_argument(
        "--udp-audio-port",
        type=int,
        help="Send raw audio to UDP port outside ASR listening",
    )

    hermes_cli.add_hermes_args(parser)
    args = parser.parse_args()

    hermes_cli.setup_logging(args)
    _LOGGER.debug(args)

    if args.list_devices:
        # List available input devices and exit
        list_devices()
        return

    # Verify arguments
    if not args.list_devices and (
        (args.sample_rate is None)
        or (args.sample_width is None)
        or (args.channels is None)
    ):
        _LOGGER.fatal("--sample-rate, --sample-width, and --channels are required")
        sys.exit(1)

    # Listen for messages
    client = mqtt.Client()
    hermes = MicrophoneHermesMqtt(
        client,
        args.sample_rate,
        args.sample_width,
        args.channels,
        device_index=args.device_index,
        site_ids=args.site_id,
        output_site_id=args.output_site_id,
        udp_audio_host=args.udp_audio_host,
        udp_audio_port=args.udp_audio_port,
    )

    _LOGGER.debug("Connecting to %s:%s", args.host, args.port)
    hermes_cli.connect(client, args)
    client.loop_start()

    try:
        # Run event loop
        asyncio.run(hermes.handle_messages_async())
    except KeyboardInterrupt:
        pass
    finally:
        _LOGGER.debug("Shutting down")
        client.loop_stop()


# -----------------------------------------------------------------------------


def list_devices():
    """Prints available input devices."""
    import pyaudio

    audio = pyaudio.PyAudio()

    print("index\tname")
    for device_index in range(audio.get_device_count()):
        device_info = audio.get_device_info_by_index(device_index)
        device_name = device_info.get("name")
        print(f"{device_index}\t{device_name}")


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
