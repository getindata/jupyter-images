#!/usr/bin/bash -i

MLFLOW_HOME=/home/jovyan/mlflow

mkdir -p ${MLFLOW_HOME}
mlflow server --host 0.0.0.0 \
    --default-artifact-root ${MLFLOW_HOME}/artifacts \
    --backend-store-uri sqlite:///${MLFLOW_HOME}/mlflow.db \
    >> /tmp/mlflow.logs 2>&1 &
