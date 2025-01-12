# ZryteZene CLI in Python

## Overview
`zz-cli-python` is a text-based command-line interface written in Python, it uses the `requests` module to communicate with Firebase features via REST, and uses [`python-vlc`](https://pypi.org/project/python-vlc) as it's audio backend.

> [!NOTE]
> This client is *read-only*, which means no authentication is required
> and the upload feature is completely absent.

## Usage
List all music entries:
```sh
$ zryte-cli list
```

Play a song via ID:
```sh
$ zryte-cli stream <id>
```

## Requirements
- Python 3.10 or greater

### Dependencies
Use `requirements.txt` to install required dependencies:
```sh
$ pip install -r requirements.txt
```

## Installation
### Windows
This client does not have a proper installer for Windows, you can clone the repository and install [required dependencies](#dependencies) instead.

### GNU/Linux
Under construction!

### macOS
Under construction!

## License
This project is licensed under the [GNU GPL V3](LICENSE) license.
