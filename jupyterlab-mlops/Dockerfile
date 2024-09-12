ARG BASE_IMAGE
FROM $BASE_IMAGE
#inputs
ARG MLFLOW_VERSION \
    KEDRO_VERSION \
    VSCODE_VERSION \
    PYTHON_VERSION \
    SPARK_SUPPORT \
    USER \
    UID \
    GID

ENV NB_USER=$USER \
    NB_UID=$UID \
    NB_GID=$GID \
    CONDA_DIR=/opt/conda \
    VSCODE_VERSION=$VSCODE_VERSION \
    KEDRO_VERSION=$KEDRO_VERSION

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
    unzip -p /usr/local/spark/jars/spark-core_2.12-3.2.0.jar \
        org/apache/spark/ui/static/stagepage.js \
        > /tmp/patches/org/apache/spark/ui/static/stagepage.js && \
    unzip -p /usr/local/spark/jars/spark-core_2.12-3.2.0.jar \
        org/apache/spark/ui/static/utils.js \
        > /tmp/patches/org/apache/spark/ui/static/utils.js && \
    patch /tmp/patches/org/apache/spark/ui/static/stagepage.js < /tmp/patches/stagepage.js.patch && \
    patch /tmp/patches/org/apache/spark/ui/static/utils.js < /tmp/patches/utils.js.patch && \
    pushd /tmp/patches && \
    zip -u /usr/local/spark/jars/spark-core_2.12-3.2.0.jar org/apache/spark/ui/static/* && \
    popd && \
    cp /tmp/patches/spark-executor-entrypoint.bash /usr/local/bin/executor && \
    cp /tmp/patches/spark-driver-entrypoint.sh /usr/local/bin/driver && \
    rm -rf /tmp/patches /var/lib/apt/lists/* ; \
    fi

# delete user jupyter,jovyan if exists
RUN  if [ "$( id ${NB_USER} 2>/dev/null | wc -l)" -eq 1 ]; then userdel ${NB_USER}; fi; \
     if [ "$( id jovyan 2>/dev/null | wc -l)" -eq 1 ]; then userdel jovyan; fi; \
     echo "add group GID if not exists (for Vertex)"; \
     if [ "$( grep ${NB_GID} /etc/group | wc -l)" -eq 0 ]; then \
        groupadd -g ${NB_GID} jupyter-group; fi; \
     echo "add user ${NB_USER} if not exits"; \
     if [ "$( id ${NB_USER} 2>/dev/null | wc -l)" -eq 0 ]; then \
        useradd -ms /bin/bash -u ${NB_UID} ${NB_USER} -g ${NB_GID}; fi; \
     echo "allow passwordless sudo and add group required by kubeflow"; \
     echo "${NB_USER} ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook && \
     groupadd -g 1337 nbusers

#install mamba if not exists
RUN if [ "$( which mamba | wc -l )" -eq 0 ]; then conda install mamba -n base -c conda-forge; fi

#copy fix-permissions
COPY resources/jupyter/fix-permissions /usr/local/bin/fix-permissions
RUN chmod 755 /usr/local/bin/fix-permissions

# copy mlflow logo and start script
COPY resources/mlflow/start-mlflow.sh /usr/local/bin
COPY resources/mlflow/logo.svg /usr/local/share/mlflow-logo.svg

# copy mlflow logo and start script
COPY resources/vscode/start-vscode.sh /usr/local/bin
COPY resources/vscode/logo.svg /usr/local/share/vscode-logo.svg

#vs code
RUN if [ "$VSCODE_VERSION" != "NONE" ]; then \
      cd /opt/ && \
      wget -nv https://github.com/cdr/code-server/releases/download/v${VSCODE_VERSION}/code-server-${VSCODE_VERSION}-linux-amd64.tar.gz && \
      tar zxvf code-server-${VSCODE_VERSION}-linux-amd64.tar.gz && \
      ln -s /opt/code-server-${VSCODE_VERSION}-linux-amd64 /opt/code-server  && \
      rm -rf code-server-${VSCODE_VERSION}-linux-amd64.tar.gz ; \
    fi

RUN sudo usermod -a -G users ${NB_USER}; \
    if [ ${NB_USER} != "jovyan" ]; then \
        if [ -d /home/jovyan ]; then \
            cp -r /home/jovyan /home/${NB_USER}; \
            chown -R ${NB_USER}:${NB_GID} /home/${NB_USER}; \
        fi; \
    fi

USER ${NB_USER}
WORKDIR /home/${NB_USER}
ENV HOME=/home/${NB_USER}
# Adding user to group that owns /opt
# That's partially because /home/jovyan is hardcoded in few parts of start scripts
# To be sure, changing ownership of old home

# install git extension
RUN pip install --no-cache-dir jupyterlab-git

USER root
# add kfp and install mlflow inside jupyterlab
RUN mamba install --quiet --yes kfp jupyter-server-proxy -c conda-forge && \
    pip --no-cache-dir install mlflow==$MLFLOW_VERSION && \
    mamba clean --all -f -y

# configure python env with optional kedro
RUN if [ "${KEDRO_VERSION}" != "NONE" ]; then \
    mamba create --quiet --yes -p "${CONDA_DIR}/envs/python${PYTHON_VERSION}" python=${PYTHON_VERSION} ipython ipykernel kedro=${KEDRO_VERSION} && \
    mamba clean --all -f -y && \
    "${CONDA_DIR}/envs/python${PYTHON_VERSION}/bin/python" -m ipykernel install --user --name=python${PYTHON_VERSION}; \
    else \
    mamba create --quiet --yes -p "${CONDA_DIR}/envs/python${PYTHON_VERSION}" python=${PYTHON_VERSION} ipython ipykernel && \
    mamba clean --all -f -y && \
    "${CONDA_DIR}/envs/python${PYTHON_VERSION}/bin/python" -m ipykernel install --user --name=python${PYTHON_VERSION}; \
    fi

RUN fix-permissions "/home/${NB_USER}" && \
    fix-permissions "${CONDA_DIR}" && \
    if [ -d /opt/jupyter ]; then chown -R ${NB_USER}:${NB_GID} /opt/jupyter; fi

USER ${NB_USER}
# above kernel installation makes sense in case of ephemeral KF notebooks (no home remounting)

COPY jupyter_server_config.py jupyter_notebook_config.py /etc/jupyter/
COPY kedro_icon_no-type_whitebg.svg /usr/local/share/kedro-logo.svg

# conda init & activate populate PATH
RUN conda config --set auto_activate_base false && \
    conda init bash && \
    echo "conda activate python${PYTHON_VERSION}" >> ~/.bashrc

ENV MLFLOW_TRACKING_URI=http://localhost:5000
ENV JUPYTER_ENABLE_LAB=yes

# Expose port for Vertex AI compatibility
EXPOSE 8080
