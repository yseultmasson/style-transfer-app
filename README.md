# Style transfer application

[![Test code quality](https://github.com/yseultmasson/mise-en-production/actions/workflows/test.yml/badge.svg)](https://github.com/yseultmasson/mise-en-production/actions/workflows/test.yml) [![Build Docker image](https://github.com/yseultmasson/style-transfer-app/actions/workflows/prod.yml/badge.svg)](https://github.com/yseultmasson/style-transfer-app/actions/workflows/prod.yml)

Matthieu Bricaire, Yseult Masson and Rayan Talate

## Project description

This project was carried out as part of the ENSAE course "Mise en production de projet data science", taught by Lino Galiana and Romain Avouac. Its aim is to build an application based on a previous project produced by Matthieu Bricaire, Yseult Masson and Rayan Talate, that [studied style transfer as a data augmentation method](https://github.com/yseultmasson/advanced-ml-project).

The application can be found at [https://styletransfer.kub.sspcloud.fr](https://styletransfer.kub.sspcloud.fr).

## Project architecture

The `src` folders contains everything related to style transfer (images preprocessing, model training, evaluation on new images). We stored the trained models at `https://minio.lab.sspcloud.fr/mbricaire/mise-en-production/models` and use them in the app.

The main code for the streamlit app is in `app.py`. The application is hosted on the SSP Cloud servers, and is continuously deployed with ArgoCD via the [GitOps repository](https://github.com/yseultmasson/style-transfer-app-deployment).

## General steps to modify the app (for contributors)

1. Create a new branch.
2. Update `app.py`.
3. Check the modifications by running `streamlit run app.py --server.port=8000 --server.address=0.0.0.0`. If `http://0.0.0.0:8000` does not work, use `http://localhost:8000` to visualize the app in a browser.
4. Once happy, commit and push the modifications.
5. Tag the new commit and push the tag by doing :
   ```bash
   git tag v1.0.0
   git push --tags
   ```
   Replace `v1.0.0` with the version you need.
7. Merge with the main branch.
8. In the file `deployment/deployment.yaml` of the [GitOps repository](https://github.com/yseultmasson/style-transfer-app-deployment), replace the image version with the new one:
   ```deployment/deployment.yaml
   ...
   spec:
      containers:
      - name: style-transfer
        image: mattbricaire/mise-en-production:v1.0.0 <- replace version here
        ports:
        - containerPort: 8000
   ```
