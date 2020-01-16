# Rhasspy PyAudio Hermes MQTT Service

Records audio from [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/) and publishes WAV chunks according to the [Hermes protocol](https://docs.snips.ai/reference/hermes).

## Running With Docker

```bash
docker run -it rhasspy/rhasspy-microphone-pyaudio-hermes:<VERSION> <ARGS>
```

## Building From Source

Clone the repository and create the virtual environment:

```bash
git clone https://github.com/rhasspy/rhasspy-microphone-pyaudio-hermes.git
cd rhasspy-microphone-pyaudio-hermes
make venv
```

Run the `bin/rhasspy-microphone-pyaudio-hermes` script to access the command-line interface:

```bash
bin/rhasspy-microphone-pyaudio-hermes --help
```

## Building the Debian Package

Follow the instructions to build from source, then run:

```bash
source .venv/bin/activate
make debian
```

If successful, you'll find a `.deb` file in the `dist` directory that can be installed with `apt`.

## Building the Docker Image

Follow the instructions to build from source, then run:

```bash
source .venv/bin/activate
make docker
```

This will create a Docker image tagged `rhasspy/rhasspy-microphone-pyaudio-hermes:<VERSION>` where `VERSION` comes from the file of the same name in the source root directory.

NOTE: If you add things to the Docker image, make sure to whitelist them in `.dockerignore`.

## Command-Line Options

```
usage: rhasspy-microphone-cli-hermes [-h] [--list-devices]
                                     [--device-index DEVICE_INDEX]
                                     --sample-rate SAMPLE_RATE --sample-width
                                     SAMPLE_WIDTH --channels CHANNELS
                                     [--host HOST] [--port PORT]
                                     [--siteId SITEID] [--debug]

optional arguments:
  -h, --help            show this help message and exit
  --list-devices        List available microphones and exit
  --device-index DEVICE_INDEX
                        Index of microphone to use (see --list-devices)
  --sample-rate SAMPLE_RATE
                        Sample rate of recorded audio in hertz (e.g., 16000)
  --sample-width SAMPLE_WIDTH
                        Sample width of recorded audio in bytes (e.g., 2)
  --channels CHANNELS   Number of channels in recorded audio (e.g., 1)
  --host HOST           MQTT host (default: localhost)
  --port PORT           MQTT port (default: 1883)
  --siteId SITEID       Hermes siteId of this server
  --debug               Print DEBUG messages to the console
```
