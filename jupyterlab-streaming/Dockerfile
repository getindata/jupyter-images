FROM jupyter/base-notebook:python-3.8

ENV TZ=US/Arizona
ENV MAVEN_CLI_OPTS="--batch-mode --errors --fail-at-end --show-version -DinstallAtEnd=true -DdeployAtEnd=true"
ENV FLINK_HOME="/opt/conda/lib/python3.8/site-packages/pyflink"
ARG PYFLINK_LIB_DIR="/opt/conda/lib/python3.8/site-packages/pyflink/lib/"

USER root

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN echo "jovyan ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook && \
    groupadd -g 1337 nbusers
COPY resources/logos/flink.svg /opt/logos/
COPY resources/jupyter_server_config_append /var/tmp/jupyter/
RUN cat /var/tmp/jupyter/jupyter_server_config_append >> /etc/jupyter/jupyter_server_config.py && \
    rm /var/tmp/jupyter/jupyter_server_config_append
RUN sudo apt update -y && \
    sudo apt-get install -y git maven openjdk-11-jdk vim curl wget && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir /opt/kafka && \
    chown jovyan:root /opt/kafka && \
    chmod 770 /opt/kafka

USER jovyan

RUN wget -O /opt/kafka/kafka.tgz https://archive.apache.org/dist/kafka/3.4.0/kafka_2.13-3.4.0.tgz && \
    tar -xzf /opt/kafka/kafka.tgz -C /opt/kafka && \
    rm /opt/kafka/kafka.tgz

RUN pip install --no-cache-dir \
    jupyterlab==$(conda list -f jupyterlab --json | grep -oP '(?<=\"version\": \")[^\"]*') \
    jupyterlab-git \
    jupyterlab-lsp \
    jupyter-server-proxy 

COPY requirements.txt .
RUN pip install pip --upgrade \
  && pip install --no-cache-dir -r requirements.txt \
  && pip cache purge \
  && rm requirements.txt


RUN mkdir -p /var/tmp/flink-deps/
COPY ./pom.xml /var/tmp/flink-deps/pom.xml
RUN mvn $MAVEN_CLI_OPTS -f /var/tmp/flink-deps/pom.xml  dependency:copy-dependencies -DoutputDirectory=$PYFLINK_LIB_DIR && \
    rm -rf ~/.m2/repository && rm -rf /var/tmp/flink-deps
