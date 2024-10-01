ARG BASE_IMAGE
FROM $BASE_IMAGE
#inputs
ARG MLFLOW_VERSION \
    KEDRO_VERSION \
    VSCODE_VERSION \
    PYTHON_VERSION \
    USER \
    UID \
    GID

ENV NB_USER=$USER \
    HOME=/home/$USER \
    NB_UID=$UID \
    NB_GID=$GID \
    CONDA_DIR=/opt/conda \
    JUPYTER_ENABLE_LAB=yes \
    VSCODE_VERSION=$VSCODE_VERSION \
    KEDRO_VERSION=$KEDRO_VERSION \
    KEDRO_DISABLE_TELEMETRY=true \
    MLFLOW_TRACKING_URI=http://localhost:5000

USER root

#install mamba if not exists
RUN if [ "$( which mamba | wc -l )" -eq 0 ]; then conda install mamba -n base -c conda-forge; fi

# copy mlflow logo and start script
COPY resources/mlflow/start-mlflow.sh /usr/local/bin
COPY resources/mlflow/logo.svg /usr/local/share/mlflow-logo.svg

# copy vscode logo and start script
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

# this should be applied but it creates huge image size so we fix only permissions
## grant sudo, fix ownerships, create ${NB_USER} if other than jovyan
#RUN GRANT_SUDO=yes \
#    CHOWN_HOME=yes \
#    CHOWN_HOME_OPTS=-R \
#    CHOWN_EXTRA=/opt/conda/share/jupyter \
#    CHOWN_EXTRA_OPTS=-R \
#    start.sh

# grant sudo, create ${NB_USER} if other than jovyan
RUN GRANT_SUDO=yes \
    start.sh

# fix: https://github.com/jupyter/docker-stacks/issues/1657#issuecomment-1156852517
RUN sed 's/jovyan 2/$NB_USER 2/g' -i /usr/local/bin/start.sh

USER ${NB_USER}
WORKDIR /home/${NB_USER}

# install git extension
RUN pip install --no-cache-dir jupyterlab-git

USER root
# add kfp and install mlflow inside jupyterlab
RUN mamba install --quiet --yes kfp jupyter-server-proxy -c conda-forge && \
    pip --no-cache-dir install mlflow==$MLFLOW_VERSION && \
    mamba clean --all -f -y

# configure python env with kedro
RUN mamba install --quiet --yes ipython ipykernel kedro=${KEDRO_VERSION} kedro-viz && \
    mamba clean --all -f -y && \
    "${CONDA_DIR}/bin/python" -m ipykernel \
    install --prefix ${CONDA_DIR} --name=python${PYTHON_VERSION}

# fix permissions
RUN fix-permissions "/home/${NB_USER}" && \
    fix-permissions "${CONDA_DIR}/share/jupyter"

USER ${NB_USER}

COPY jupyter_server_config.py jupyter_notebook_config.py /etc/jupyter/
COPY kedro_icon_no-type_whitebg.svg /usr/local/share/kedro-logo.svg

# conda init & activate populate PATH
RUN conda init bash

# Expose port for Vertex AI compatibility
EXPOSE 8080
