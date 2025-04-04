ARG VSCODE_VERSION=4.14.1
ARG VSCODE_PYTHON=2023.10.1
ARG VSCODE_DBT_POWER_USER=0.13.0
ARG VSCODE_DBT=1.4
ARG DP_CLI_VERSION=0.26.0

FROM gcr.io/deeplearning-platform-release/base-cpu.py310:m108 as base

ARG VSCODE_VERSION
ARG VSCODE_PYTHON
ARG VSCODE_DBT_POWER_USER
ARG VSCODE_DBT

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    curl \
    git \
    openjdk-11-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# code server
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version ${VSCODE_VERSION} && \
    rm -rf "${HOME}/.cache"
RUN code-server --install-extension ms-python.python${VSCODE_PYTHON} \
    code-server --install-extension innoverio.vscode-dbt-power-user@${VSCODE_DBT_POWER_USER} \
    code-server --install-extension bastienboutonnet.vscode-dbt@${VSCODE_DBT}
COPY resources/vsc/settings.json /root/.local/share/code-server/Machine/
COPY resources/vsc/.bashrc root/

# requirements
COPY requirements/requirements.txt /opt/requirements/
RUN pip install -r /opt/requirements/requirements.txt

# logos
COPY resources/logos/ /opt/logos/

# jupyter config
COPY resources/jupyter/gcp/ /etc/jupyter/

# Expose port for Vertex AI compatibility
EXPOSE 8080

FROM base as gcp
COPY requirements/requirements-bigquery.txt /opt/requirements/
RUN pip install -r /opt/requirements/requirements-bigquery.txt
# NOTE: gcp image is currently not built due to discontinued support for custom images in Vertex AI

# Jupyterhub version
FROM jupyter/minimal-notebook:python-3.11.4 as jupyterhub-base

ARG VSCODE_VERSION
ARG DP_CLI_VERSION

USER root
RUN echo "jovyan ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/notebook && \
    groupadd -g 1337 nbusers

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    curl \
    git \
    g++ \
    openjdk-11-jdk \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN chown -R jovyan:users $HOME
USER jovyan
# install python packages
RUN pip install --no-cache-dir \
    jupyterlab==$(conda list -f jupyterlab --json | grep -oP '(?<=\"version\": \")[^\"]*') \
    jupyterlab-git

# BIGQUERY-POSTGRES
FROM jupyterhub-base as bigquery-postgres
USER root
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    gnupg \
    sudo

RUN echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    google-cloud-cli \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER jovyan
# install python packages
RUN pip install --no-cache-dir \
    'google-cloud-bigquery[bqstorage,pandas]' \
    ipywidgets \
    psycopg2 \
    ipython-sql

# WORKSHOP-BIGQUERY
FROM jupyterhub-base AS workshop-bigquery
USER jovyan
ARG VSCODE_VERSION
ARG DP_CLI_VERSION
RUN pip install --no-cache-dir \
    jupyter-server-proxy \
    data-pipelines-cli[docker,datahub,gcs,bigquery]==${DP_CLI_VERSION} \
    sqlfluff==2.3.0

USER root
RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    apt-transport-https \
    ca-certificates \
    gnupg \
    sudo

RUN echo "deb https://packages.cloud.google.com/apt cloud-sdk main" | sudo tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    google-cloud-cli \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY resources/logos/ /opt/logos/
COPY resources/jupyter/ resources/vsc/addons/ resources/vsc/jupyterhub/settings.json resources/vsc/.bashrc  /var/tmp/
RUN cat /var/tmp/jupyterhub/jupyter_server_config_append >> /etc/jupyter/jupyter_server_config.py
RUN chown -R jovyan:users $HOME

USER jovyan
# install python packages
RUN pip install --no-cache-dir \
    'google-cloud-bigquery[bqstorage,pandas]' \
    ipywidgets \
    psycopg2 \
    ipython-sql
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version ${VSCODE_VERSION}
RUN code-server --extensions-dir /var/tmp/extension --install-extension ms-python.python \
    code-server --extensions-dir /var/tmp/extension --install-extension innoverio.vscode-dbt-power-user \
    code-server --extensions-dir /var/tmp/extension --install-extension /var/tmp/bastienboutonnet.vscode-dbt-0.5.1.vsix

# SNOWFLAKE
FROM jupyterhub-base as snowflake
USER jovyan
ARG VSCODE_VERSION
ARG DP_CLI_VERSION
RUN pip install --no-cache-dir \
    jupyter-server-proxy \
    data-pipelines-cli[docker,datahub,s3,snowflake]==${DP_CLI_VERSION} \
    sqlfluff==2.3.0

USER root
# Copies your code file  repository to the filesystem
COPY resources/snowsql/entrypoint.sh /entrypoint.sh
# change permission to execute the script and
RUN chmod +x /entrypoint.sh
# logos
COPY resources/logos/ /opt/logos/
# copy snowsql config jupyter config, addons and settings.json for code server
COPY resources/snowsql/config resources/jupyter/ resources/vsc/addons/ resources/vsc/jupyterhub/settings.json resources/vsc/.bashrc  /var/tmp/
# add additional config
RUN cat /var/tmp/jupyterhub/jupyter_server_config_append >> /etc/jupyter/jupyter_server_config.py
# download snowsql binaries
RUN curl -o /usr/bin/snowsql-1.2.24-linux_x86_64.bash https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowsql-1.2.24-linux_x86_64.bash && \
    chmod a+x /usr/bin
# initialize snosql binariers
RUN SNOWSQL_DEST=/var/tmp/bin SNOWSQL_LOGIN_SHELL=/etc/bash.bashrc bash /usr/bin/snowsql-1.2.24-linux_x86_64.bash

RUN chown -R jovyan:users $HOME
USER jovyan

# install code server and addons
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version ${VSCODE_VERSION}
RUN code-server --extensions-dir /var/tmp/extension --install-extension ms-python.python \
    code-server --extensions-dir /var/tmp/extension --install-extension innoverio.vscode-dbt-power-user \
    code-server --extensions-dir /var/tmp/extension --install-extension /var/tmp/snowflake.snowflake-vsc-0.5.2.vsix \
    code-server --extensions-dir /var/tmp/extension --install-extension /var/tmp/bastienboutonnet.vscode-dbt-0.5.1.vsix

ENTRYPOINT [ "/entrypoint.sh" ]
