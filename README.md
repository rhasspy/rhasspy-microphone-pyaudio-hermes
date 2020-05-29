# Rhasspy PyAudio Hermes MQTT Service

[![Continous Integration](https://github.com/rhasspy/rhasspy-microphone-pyaudio-hermes/workflows/Tests/badge.svg)](https://github.com/rhasspy/rhasspy-microphone-pyaudio-hermes/actions)
[![GitHub license](https://img.shields.io/github/license/rhasspy/rhasspy-microphone-pyaudio-hermes.svg)](https://github.com/rhasspy/rhasspy-microphone-pyaudio-hermes/blob/master/LICENSE)

Records audio from [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) and publishes WAV chunks according to the [Hermes protocol](https://docs.snips.ai/reference/hermes).

## Running With Docker

```bash
$ docker run -it rhasspy/rhasspy-microphone-pyaudio-hermes:<VERSION> <ARGS>
```

## Building From Source

Clone the repository and create the virtual environment:

```bash
$ git clone https://github.com/rhasspy/rhasspy-microphone-pyaudio-hermes.git
$ cd rhasspy-microphone-pyaudio-hermes
$ ./configure --enable-in-place
$ make
$ make install
```

Run the `rhasspy-microphone-pyaudio-hermes` script to access the command-line interface:

```bash
$ ./rhasspy-microphone-pyaudio-hermes --help
```

## Building the Docker Image

Run `scripts/build-docker.sh` with a local docker registry:

```bash
$ DOCKER_REGISTRY=myregistry:12345 scripts/build-docker.sh
```

Requires [Docker Buildx](https://docs.docker.com/buildx/working-with-buildx/). Set `PLATFORMS` environment to only build for specific platforms (e.g., `linux/amd64`).

This will create a Docker image tagged `rhasspy/rhasspy-microphone-pyaudio-hermes:<VERSION>` where `VERSION` comes from the file of the same name in the source root directory.

NOTE: If you add things to the Docker image, make sure to whitelist them in `.dockerignore`.

## Command-Line Options

```
usage: rhasspy-microphone-pyaudio-hermes [-h] [--list-devices]
                                         [--device-index DEVICE_INDEX]
                                         [--sample-rate SAMPLE_RATE]
                                         [--sample-width SAMPLE_WIDTH]
                                         [--channels CHANNELS]
                                         [--output-site-id OUTPUT_SITE_ID]
                                         [--udp-audio-host UDP_AUDIO_HOST]
                                         [--udp-audio-port UDP_AUDIO_PORT]
                                         [--host HOST] [--port PORT]
                                         [--username USERNAME]
                                         [--password PASSWORD]
                                         [--site-id SITE_ID] [--debug]
                                         [--log-format LOG_FORMAT]

optional arguments:
  -h, --help            show this help message and exit
  --list-devices        List available input devices
  --device-index DEVICE_INDEX
                        Index of microphone to use
  --sample-rate SAMPLE_RATE
                        Sample rate of recorded audio in hertz (e.g., 16000)
  --sample-width SAMPLE_WIDTH
                        Sample width of recorded audio in bytes (e.g., 2)
  --channels CHANNELS   Number of channels in recorded audio (e.g., 1)
  --output-site-id OUTPUT_SITE_ID
                        If set, output audio data to a different site id
  --udp-audio-host UDP_AUDIO_HOST
                        Host for UDP audio (default: 127.0.0.1)
  --udp-audio-port UDP_AUDIO_PORT
                        Send raw audio to UDP port outside ASR listening
  --host HOST           MQTT host (default: localhost)
  --port PORT           MQTT port (default: 1883)
  --username USERNAME   MQTT username
  --password PASSWORD   MQTT password
  --site-id SITE_ID     Hermes site id(s) to listen for (default: all)
  --debug               Print DEBUG messages to the console
  --log-format LOG_FORMAT
                        Python logger format
```
