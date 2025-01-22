# IIIS Seminar Watcher
[![CI](https://github.com/ODearEvanHansen/iiis-watcher/actions/workflows/ci.yml/badge.svg)](https://github.com/ODearEvanHansen/iiis-watcher/actions/workflows/ci.yml)

A tool to monitor IIIS seminars and send email notifications when new seminars are added.

## Description
The IIIS Seminar Watcher is a Python-based tool that automatically monitors the IIIS seminar schedule and sends email notifications when new seminars are added. It's particularly useful for staying updated with the latest research talks and events.

## Installation
```bash
pip install iiis-watcher
```

## Usage
```python
from iiis_watcher import Watcher

# Initialize watcher
watcher = Watcher()

# Start monitoring
watcher.start()
```

## Contributing
We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.