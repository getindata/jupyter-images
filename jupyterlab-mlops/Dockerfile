ARG BASE_IMAGE
FROM $BASE_IMAGE

#inputs
ARG MLFLOW_VERSION
ARG KEDRO_VERSION
ARG SPARK_SUPPORT

ENV NB_USER=jovyan
ENV NB_UID=1000
ENV NB_GID=100
ENV CONDA_DIR=/opt/conda

USER root

# patch spark UI (https://github.com/jupyterhub/jupyter-server-proxy/issues/57)
COPY patches/ /tmp/patches
COPY spark-executor-entrypoint.bash /tmp/patches/
COPY spark-driver-entrypoint.sh /tmp/patches/

RUN if [ "$SPARK_SUPPORT" = "true" ]; then \
    apt clean && \
    apt update --fix-missing && \
    apt install -y zip patch && \
    mkdir -p /tmp/patches/org/apache/spark/ui/static/ && \
    unzip -p /usr/local/spark/jars/spark-core_2.12-3.2.0.jar org/apache/spark/ui/static/stagepage.js > /tmp/patches/org/apache/spark/ui/static/stagepage.js && \
    unzip -p /usr/local/spark/jars/spark-core_2.12-3.2.0.jar org/apache/spark/ui/static/utils.js > /tmp/patches/org/apache/spark/ui/static/utils.js && \
    patch /tmp/patches/org/apache/spark/ui/static/stagepage.js < /tmp/patches/stagepage.js.patch && \
    patch /tmp/patches/org/apache/spark/ui/static/utils.js < /tmp/patches/utils.js.patch && \
    pushd /tmp/patches && \
    zip -u /usr/local/spark/jars/spark-core_2.12-3.2.0.jar org/apache/spark/ui/static/* && \
    popd && \
    cp /tmp/patches/spark-executor-entrypoint.bash /usr/local/bin/executor && \
    cp /tmp/patches/spark-driver-entrypoint.sh /usr/local/bin/driver && \
    rm -rf /tmp/patches /var/lib/apt/lists/* ; \
    fi

# add user $NB_USER if not exits
RUN  if [ "$( id $NB_USER 2>/dev/null | wc -l)" -eq 0 ]; then useradd -ms /bin/bash $NB_USER; fi

# allow passwordless sudo and add group required by kubeflow
RUN echo "$NB_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook && \
    groupadd -g 1337 nbusers

#install mamba if not exists
RUN if [ "$( which mamba | wc -l )" -eq 0 ]; then conda install mamba -n base -c conda-forge && chmod 777 -R /opt/conda/; fi

#copy fix-permissions
COPY resources/jupyter/fix-permissions /usr/local/bin/fix-permissions
RUN chmod 755 /usr/local/bin/fix-permissions

# copy mlflow logo and start script
COPY mlflow/start-mlflow.sh /usr/local/bin
COPY mlflow/logo.svg /usr/local/share/mlflow-logo.svg

USER $NB_USER

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

ENV PATH "${PATH}:${CONDA_DIR}/envs/python38/bin"
ENV CONDA_DEFAULT_ENV python38
ENV MLFLOW_TRACKING_URI=http://localhost:5000
ENV JUPYTER_ENABLE_LAB=yes

# Expose port for Vertex AI compatibility
EXPOSE 8080
