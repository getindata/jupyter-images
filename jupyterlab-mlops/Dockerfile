ARG BASE_IMAGE
FROM $BASE_IMAGE
#inputs
ARG MLFLOW_VERSION \
    KEDRO_VERSION \
    VSCODE_VERSION \
    SPARK_SUPPORT \
    USER=jupyter \
    UID=1000 \
    GID=100
 
ENV NB_USER=$USER \ 
    NB_UID=$UID \
    NB_GID=$GID \
    CONDA_DIR=/opt/conda \
    VSCODE_VERSION=$VSCODE_VERSION

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

# delete user jupyter,jovyan if exists
RUN  if [ "$( id $NB_USER 2>/dev/null | wc -l)" -eq 1 ]; then userdel $NB_USER; fi; \
     if [ "$( id jovyan 2>/dev/null | wc -l)" -eq 1 ]; then userdel jovyan; fi; \
     echo  add user $NB_USER if not exits; \ 
     if [ "$( id $NB_USER 2>/dev/null | wc -l)" -eq 0 ]; then useradd -ms /bin/bash -u $NB_UID $NB_USER; fi; \
     echo "add group GID 1001 if not exists (for Vertex)"; \
     if [ "$( grep 1001 /etc/group | wc -l)" -eq 0 ]; then groupadd -g 1001 jupyter-group; fi; \
     echo "allow passwordless sudo and add group required by kubeflow"; \
     echo "$NB_USER ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook && \
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

RUN sudo usermod -a -G users $NB_USER; \
    if [ -d /home/jovyan ]; then cp -r /home/jovyan /home/$NB_USER; fi; \
    if [ -d /home/jovyan ]; then chown -R $NB_UID:$NB_USER /home/jovyan; fi; \
    chown -R $NB_USER:$NB_USER /home/$NB_USER

USER $NB_USER
WORKDIR /home/$NB_USER
ENV HOME=/home/$NB_USER \
    PATH=$PATH:/home/$NB_USER/.local/bin
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

# configure python 3.8 env with kedro
RUN mamba create --quiet --yes -p "${CONDA_DIR}/envs/python38" python=3.8 ipython ipykernel kedro=$KEDRO_VERSION && \
    mamba clean --all -f -y && \
    "${CONDA_DIR}/envs/python38/bin/python" -m ipykernel install --user --name=python38

RUN fix-permissions "/home/${NB_USER}" && \
    fix-permissions "${CONDA_DIR}" && \
    chown -R $NB_USER:$NB_USER $HOME && \
    if [ -e /usr/local/bin/start-notebook.sh ]; then sed 's/jupyter lab/jupyter lab $NOTEBOOK_ARGS/g' /usr/local/bin/start-notebook.sh -i; fi
RUN if [ -d /otp/jupyter ]; then chown -R $NB_USER:$NB_USER /opt/jupyter; fi
USER $NB_USER
# above kernel installation makes sense in case of ephemeral KF notebooks (no home remounting)

COPY jupyter_server_config.py jupyter_notebook_config.py /etc/jupyter/
COPY kedro_icon_no-type_whitebg.svg /usr/local/share/kedro-logo.svg

ENV PATH "${PATH}:${CONDA_DIR}/envs/python38/bin"
ENV CONDA_DEFAULT_ENV python38
ENV MLFLOW_TRACKING_URI=http://localhost:5000
ENV JUPYTER_ENABLE_LAB=yes

# Expose port for Vertex AI compatibility
 EXPOSE 8080
