# mise-en-production

[![Code quality testing](https://github.com/yseultmasson/mise-en-production/actions/workflows/test.yml/badge.svg)](https://github.com/yseultmasson/mise-en-production/actions/workflows/test.yml)

To build the docker image manually:
```bash
docker build . -t mise-en-production
```

Since the CI is set up, you can also pull our docker images from the hub. For instance, you can collect the `v0.0.1` version by running:

```bash
docker pull mattbricaire/mise-en-production:v0.0.1
```

To run a container:
```bash
docker run -p 8000:8000 mattbricaire/mise-en-production:v0.0.1
```

Replace `mattbricaire/mise-en-production:v0.0.1` by `mise-en-production` if you are using the manually built image.

To visualize the app in a browser, go to `http://localhost:8000` if `http://0.0.0.0:8000` does not work.