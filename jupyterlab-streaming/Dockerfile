FROM gcr.io/getindata-images-public/jupyterlab-base:ubuntu-20.04.python-3.8
ARG VSCODE_VERSION=4.9.1
ARG VSCODE_PYTHON=2022.13.12141005
ARG STREAMING_CLI_VERSION=1.6.0
ARG MAGIC_VERSION=0.12.1
ENV TZ=Etc/UTC
ENV MAVEN_CLI_OPTS="--batch-mode --errors --fail-at-end --show-version -DinstallAtEnd=true -DdeployAtEnd=true"
ENV FLINK_HOME="/opt/conda/lib/python3.8/site-packages/pyflink"
ENV HADOOP_CONF_DIR="/etc/hadoop/conf"
ARG PYFLINK_LIB_DIR="/opt/conda/lib/python3.8/site-packages/pyflink/lib/"

USER root
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN echo "jovyan ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook && \
    groupadd -g 1337 nbusers

# logos
COPY resources/logos/ /opt/logos/

# jupyter config
COPY resources/jupyter /var/tmp/jupyter/
RUN cat /var/tmp/jupyter/jupyter_server_config_append >> /etc/jupyter/jupyter_server_config.py

RUN sudo apt update -y && \
    sudo apt-get install -y git maven openjdk-11-jdk curl && \
    rm -rf /var/lib/apt/lists/*

# code server
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version ${VSCODE_VERSION} && \
    rm -rf "${HOME}/.cache"
RUN code-server --install-extension ms-python.python${VSCODE_PYTHON}
COPY resources/vsc/settings.json /root/.local/share/code-server/Machine/
COPY resources/vsc/.bashrc root/

RUN chown jovyan:users -R /home/jovyan/.local

USER jovyan
RUN pip install --no-cache-dir \
    jupyterlab==$(conda list -f jupyterlab --json | grep -oP '(?<=\"version\": \")[^\"]*') \
    jupyterlab-git \
    jupyterlab-lsp \
    jupyter-server-proxy
RUN pip install --no-cache-dir streamingcli==${STREAMING_CLI_VERSION}
RUN pip install --no-cache-dir jupyter-packaging==0.12.2 
RUN pip install --no-cache-dir streaming-jupyter-integrations==${MAGIC_VERSION}
RUN pip uninstall -y jupyter-core && pip install --no-cache-dir jupyter-core
RUN pip cache purge

RUN mkdir -p /var/tmp/flink-deps/
COPY ./pom.xml /var/tmp/flink-deps/pom.xml
RUN mvn $MAVEN_CLI_OPTS -f /var/tmp/flink-deps/pom.xml dependency:copy-dependencies -DoutputDirectory=$PYFLINK_LIB_DIR && \
    rm -rf ~/.m2/repository && rm -rf /var/tmp/flink-deps

EXPOSE 8080/tcp
