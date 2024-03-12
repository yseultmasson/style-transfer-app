# mise-en-production

[![Code quality testing](https://github.com/yseultmasson/mise-en-production/actions/workflows/test.yml/badge.svg)](https://github.com/yseultmasson/mise-en-production/actions/workflows/test.yml)

To build the docker image manually:
```bash
docker build . -t style-transfer-image
```

To run a container:
```bash
docker run -p 8000:8000 style-transfer-image
```
