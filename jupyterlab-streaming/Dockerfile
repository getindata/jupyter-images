FROM maven:3.8.3-openjdk-11 AS MAVEN_BUILD
ARG FLINK_DEPS_TMP=/var/tmp/flink-deps/

COPY pom.xml .
RUN mkdir $FLINK_DEPS_TMP
RUN mvn dependency:copy-dependencies -DoutputDirectory=$FLINK_DEPS_TMP

########################################################################
FROM jupyter/base-notebook:python-3.8

ARG VSCODE_VERSION=4.9.1
ARG VSCODE_PYTHON=2022.13.12141005
ARG PYFLINK_LIB_DIR="/opt/conda/lib/python3.8/site-packages/pyflink/lib/"
ARG KUBECTL_VERSION=v1.26.1

ENV DOCKER_STACKS_JUPYTER_CMD=lab
ENV NOTEBOOK_ARGS='--allow-root --ip 0.0.0.0 --config=/etc/jupyter/jupyter_notebook_config.py'

# jupyter home path
RUN mkdir /home/jovyan/jupyter

# for Vertex AI
EXPOSE 8080

USER root

RUN apt update -y \
    && apt-get install -y git openjdk-11-jdk curl vim \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# GH Cli
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
    && chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
    | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
    && apt update \
    && apt install gh -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# gcloud + kubectl
RUN apt-get update \
    && apt-get install -y apt-transport-https ca-certificates gnupg \
    && echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" \
    | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
    && curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
    | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - \
    && apt-get update \
    && apt-get install -y google-cloud-cli google-cloud-sdk-gke-gcloud-auth-plugin kubectl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# code server
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version ${VSCODE_VERSION} \
    && rm -rf "${HOME}/.cache"

USER jovyan

RUN code-server --install-extension ms-python.python${VSCODE_PYTHON}
COPY resources/vsc/settings.json /root/.local/share/code-server/Machine/
COPY resources/vsc/.bashrc root/

RUN pip install --no-cache-dir \
    jupyterlab==$(conda list -f jupyterlab --json | grep -oP '(?<=\"version\": \")[^\"]*') \
    jupyterlab-git \
    jupyterlab-lsp \
    jupyter-server-proxy 

RUN pip install --no-cache-dir streamingcli==2.0.3
RUN pip install --no-cache-dir jupyter-packaging==0.12.2 
RUN pip install --no-cache-dir streaming-jupyter-integrations==0.14.0 && pip cache purge
RUN pip install --no-cache-dir apache-flink==1.16.1
RUN pip install typing-extensions --upgrade

COPY --from=MAVEN_BUILD /var/tmp/flink-deps/ $PYFLINK_LIB_DIR
COPY resources/jupyter/jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py
COPY resources/logos/ /opt/logos/
