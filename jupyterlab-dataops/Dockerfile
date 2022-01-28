ARG BASE_IMAGE=jupyter/base-notebook:python-3.8.8
FROM $BASE_IMAGE

USER root
ARG PIP_VERSION=21.0.1
ARG USER_NAME=jovyan
ARG PROVIDER=""
ENV HOME=/tmp/$USER_NAME

ADD resources/bin/*.sh /opt/tools/bin/
ADD resources/logos/* /opt/tools/logos/
ADD resources/config/jupyter_notebook_config.py resources/config/jupyter_server_config.py  /etc/jupyter/
ADD resources/vsc/vsix/* /tmp/$NB_USER/vsix/
# Copy `requirements.txt` and `requirements-${PROVIDER}.txt`, if exists.
COPY requirements.txt requirements-${PROVIDER}.tx[t] $HOME/

RUN apt-get update --fix-missing && apt-get -qq -y install \
    curl \
    unzip \
    zip \
    jq \
    git && \
    rm /bin/sh && ln -s /bin/bash /bin/sh


RUN mkdir -p $HOME && chown -R $USER_NAME $HOME && \
    mkdir -p /opt/tools/{bin,logos} && \
    chmod -R 755 /opt/tools/ && \
    mkdir -p /mnt/data && chown -R $NB_USER /mnt/data

# Install Python and Jupyter extensions
RUN pip install -r $HOME/requirements.txt
RUN if [[ -z "$PROVIDER" ]] ; then echo "Argument PROVIDER not provided" ; else pip install -r $HOME/requirements-${PROVIDER}.txt ; fi
RUN jupyter labextension install @jupyterlab/server-proxy jupyterlab-topbar-extension

# Install code server
RUN cd /opt/ && wget https://github.com/cdr/code-server/releases/download/v3.12.0/code-server-3.12.0-linux-amd64.tar.gz && \
    tar zxvf code-server-3.12.0-linux-amd64.tar.gz

USER $NB_USER
RUN /opt/code-server-*-linux-amd64/bin/code-server \
    --extensions-dir $HOME/code-server/extensions \
    --user-data-dir $HOME/code-server/data \
    --config $HOME/code-server/config.yaml \
    --install-extension ms-python.python \
    /opt/code-server-*-linux-amd64/bin/code-server \
    --install-extension /tmp/$NB_USER/vsix/innoverio.vscode-dbt-power-user-0.5.9.vsix \
    /opt/code-server-*-linux-amd64/bin/code-server \
    --install-extension /tmp/$NB_USER/vsix/bastienboutonnet.vscode-dbt-0.5.1.vsix

ADD resources/vsc/settings.json $HOME/code-server/data/User/settings.json

ENV HOME=/home/$USER_NAME
ENV CODE_WORKINGDIR="${HOME}/work"
ENV PATH="${PATH}:${CONDA_DIR}/envs/python38/bin"
ENV CONDA_DEFAULT_ENV=python38
ENV JUPYTER_ENABLE_LAB=yes
# Expose port for Vertex AI compatibility
EXPOSE 8080
