cd ../../jupyterlab-mlops
docker build -t test . \
--build-arg BASE_IMAGE="jupyter/pyspark-notebook:lab-3.2.1" \
--build-arg SPARK_SUPPORT=true \
--build-arg KEDRO_VERSION=0.17.5 \
--build-arg MLFLOW_VERSION=1.21.0

cd ../../jupyterlab-mlops
docker build -t test . \
--build-arg BASE_IMAGE="gcr.io/deeplearning-platform-release/base-cpu:m88" \
--build-arg SPARK_SUPPORT=false \
--build-arg KEDRO_VERSION=0.17.5 \
--build-arg MLFLOW_VERSION=1.21.0
