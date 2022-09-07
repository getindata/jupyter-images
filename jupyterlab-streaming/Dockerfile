FROM gcr.io/getindata-images-public/jupyterlab-base:ubuntu-20.04.python-3.8
ARG STREAMING_CLI_VERSION=1.6.0
ARG MAGIC_VERSION=0.6.2
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
COPY resources/jupyter/ /etc/jupyter/

RUN sudo apt update -y && \
    sudo apt-get install -y git maven openjdk-11-jdk && \
    rm -rf /var/lib/apt/lists/*

USER jovyan
RUN pip install --no-cache-dir \
    jupyterlab==$(conda list -f jupyterlab --json | grep -oP '(?<=\"version\": \")[^\"]*') \
    jupyterlab-git \
    jupyterlab-lsp \
    jupyter-server-proxy
RUN pip install --no-cache-dir streamingcli==${STREAMING_CLI_VERSION}
RUN pip install --no-cache-dir jupyter-packaging==0.12.2 
RUN pip install --no-cache-dir streaming-jupyter-integrations==${MAGIC_VERSION} && pip cache purge

RUN mkdir -p /var/tmp/flink-deps/
COPY ./pom.xml /var/tmp/flink-deps/pom.xml
RUN mvn $MAVEN_CLI_OPTS -f /var/tmp/flink-deps/pom.xml dependency:copy-dependencies -DoutputDirectory=$PYFLINK_LIB_DIR && \
    rm -rf ~/.m2/repository && rm -rf /var/tmp/flink-deps
