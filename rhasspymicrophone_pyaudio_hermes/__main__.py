"""Hermes MQTT service for Rhasspy TTS with PyAudio."""
import argparse
import json
import logging
import sys

import paho.mqtt.client as mqtt

from . import MicrophoneHermesMqtt

_LOGGER = logging.getLogger(__name__)


def main():
    """Main method."""
    parser = argparse.ArgumentParser(prog="rhasspymicrophone_cli_hermes")
    parser.add_argument(
        "--list-devices",
        action="store_true",
        help="List available microphones and exit",
    )
    parser.add_argument(
        "--device-index", help="Index of microphone to use (see --list-devices)"
    )
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
        "--host", default="localhost", help="MQTT host (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=1883, help="MQTT port (default: 1883)"
    )
    parser.add_argument(
        "--siteId", default="default", help="Hermes siteId of this server"
    )
    parser.add_argument(
        "--debug", action="store_true", help="Print DEBUG messages to the console"
    )
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    _LOGGER.debug(args)

    if args.list_devices:
        _LOGGER.debug("Testing microphones")

        # List available microphones and exit
        result = MicrophoneHermesMqtt.test_microphones(
            args.sample_rate, args.sample_width, args.channels
        )
        json.dump(result, sys.stdout, indent=4)
        print("")
        return

    try:
        # Listen for messages
        client = mqtt.Client()
        hermes = MicrophoneHermesMqtt(
            client,
            args.sample_rate,
            args.sample_width,
            args.channels,
            device_index=args.device_index,
            siteId=args.siteId,
        )

        def on_disconnect(client, userdata, flags, rc):
            try:
                # Automatically reconnect
                _LOGGER.info("Disconnected. Trying to reconnect...")
                client.reconnect()
            except Exception:
                _LOGGER.exception("on_disconnect")

        # Connect
        client.on_connect = hermes.on_connect
        client.on_disconnect = on_disconnect

        _LOGGER.debug("Connecting to %s:%s", args.host, args.port)
        client.connect(args.host, args.port)

        client.loop_forever()
    except KeyboardInterrupt:
        pass
    finally:
        _LOGGER.debug("Shutting down")


# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()
