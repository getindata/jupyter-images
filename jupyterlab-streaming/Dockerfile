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

ENV DOCKER_STACKS_JUPYTER_CMD=lab
ENV NOTEBOOK_ARGS='--allow-root --ip 0.0.0.0 --config=/etc/jupyter/jupyter_notebook_config.py'
COPY resources/jupyter/jupyter_notebook_config.py /etc/jupyter/jupyter_notebook_config.py
COPY resources/logos/ /opt/logos/

# for Vertex AI
EXPOSE 8080

COPY requirements.txt .
RUN pip install pip --upgrade \
  && pip install --no-cache -r requirements.txt \
  && pip cache purge

USER root

RUN apt update -y \
    && apt-get install -y git openjdk-11-jdk curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# code server
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version ${VSCODE_VERSION} \
    && rm -rf "${HOME}/.cache"

USER jovyan

RUN code-server --install-extension ms-python.python${VSCODE_PYTHON}
COPY resources/vsc/settings.json /root/.local/share/code-server/Machine/
COPY resources/vsc/.bashrc root/

COPY --from=MAVEN_BUILD /var/tmp/flink-deps/ $PYFLINK_LIB_DIR
