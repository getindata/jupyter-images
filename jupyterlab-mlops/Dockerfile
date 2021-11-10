FROM jupyter/pyspark-notebook:lab-3.1.9

ARG MLFLOW_VERSION="1.21.0"
ARG KEDRO_VERSION="0.17.5"

USER root

# patch spark UI (https://github.com/jupyterhub/jupyter-server-proxy/issues/57)
COPY patches/ /tmp/patches

RUN apt update && \
    apt install -y zip patch && \
    mkdir -p /tmp/patches/org/apache/spark/ui/static/ && \
    unzip -p /usr/local/spark/jars/spark-core_2.12-3.1.2.jar org/apache/spark/ui/static/stagepage.js > /tmp/patches/org/apache/spark/ui/static/stagepage.js && \
    unzip -p /usr/local/spark/jars/spark-core_2.12-3.1.2.jar org/apache/spark/ui/static/utils.js > /tmp/patches/org/apache/spark/ui/static/utils.js && \
    patch /tmp/patches/org/apache/spark/ui/static/stagepage.js < /tmp/patches/stagepage.js.patch && \
    patch /tmp/patches/org/apache/spark/ui/static/utils.js < /tmp/patches/utils.js.patch && \
    pushd /tmp/patches && \
    zip -u /usr/local/spark/jars/spark-core_2.12-3.1.2.jar org/apache/spark/ui/static/* && \
    popd && \
    rm -rf /tmp/patches /var/lib/apt/lists/*

# allow passwordless sudo and add group required by kubeflow
RUN echo "jovyan ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook && \
    groupadd -g 1337 nbusers

# copy mlflow logo and start script
COPY mlflow/start-mlflow.sh /usr/local/bin
COPY mlflow/logo.svg /usr/local/share/mlflow-logo.svg

USER jovyan

# install git extension
RUN pip install --no-cache-dir jupyterlab-git

# add kfp and install mlflow inside jupyterlab
RUN mamba install --quiet --yes kfp jupyter-server-proxy -c conda-forge && \
    pip --no-cache-dir install mlflow==$MLFLOW_VERSION && \
    mamba clean --all -f -y 

# configure python 3.8 env with kedro
RUN mamba create --quiet --yes -p "${CONDA_DIR}/envs/python38" python=3.8 ipython ipykernel kedro=$KEDRO_VERSION && \
    mamba clean --all -f -y && \
    "${CONDA_DIR}/envs/python38/bin/python" -m ipykernel install --user --name=python38 && \
    fix-permissions "/home/${NB_USER}" && \
    fix-permissions "${CONDA_DIR}"
    
COPY jupyter_server_config.py jupyter_notebook_config.py /etc/jupyter/
COPY spark-executor-entrypoint.bash /usr/local/bin/executor

ENV PATH "${PATH}:${CONDA_DIR}/envs/python38/bin"
ENV CONDA_DEFAULT_ENV python38
ENV MLFLOW_TRACKING_URI=http://localhost:5000
ENV JUPYTER_ENABLE_LAB=yes

# Expose port for Vertex AI compatibility
EXPOSE 8080
