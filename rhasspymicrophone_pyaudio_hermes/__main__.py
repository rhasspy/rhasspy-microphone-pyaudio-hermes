"""Hermes MQTT service for Rhasspy TTS with PyAudio."""
import argparse
import asyncio
import logging

import paho.mqtt.client as mqtt
import rhasspyhermes.cli as hermes_cli

from . import MicrophoneHermesMqtt

_LOGGER = logging.getLogger(__name__)


def main():
    """Main method."""
    parser = argparse.ArgumentParser(prog="rhasspy-microphone-pyaudio-hermes")
    parser.add_argument("--device-index", type=int, help="Index of microphone to use")
    parser.add_argument(
        "--sample-rate",
        type=int,
        required=True,
        help="Sample rate of recorded audio in hertz (e.g., 16000)",
    )
    parser.add_argument(
        "--sample-width",
        type=int,
        required=True,
        help="Sample width of recorded audio in bytes (e.g., 2)",
    )
    parser.add_argument(
        "--channels",
        type=int,
        required=True,
        help="Number of channels in recorded audio (e.g., 1)",
    )
    parser.add_argument(
        "--output-site-id", help="If set, output audio data to a different site id"
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

if __name__ == "__main__":
    main()
