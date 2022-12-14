ARG VSCODE_VERSION=4.5.1
ARG VSCODE_PYTHON=2022.13.12141005
ARG VSCODE_DBT_POWER_USER=0.6.2
ARG VSCODE_DBT=0.5.1
ARG DP_CLI_VERSION=0.23.0

FROM gcr.io/deeplearning-platform-release/base-cpu:m88 as base

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

# cloudbeaver
COPY --from=gcr.io/getindata-images-public/cloudbeaver-dataops:0.1.0 /opt/cloudbeaver/ /opt/cloudbeaver/
COPY resources/cloudbeaver/conf /opt/cloudbeaver/conf

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
ADD resources/cloudbeaver/conf/initial-data-sources-bigquery.conf.j2 /opt/cloudbeaver/conf/initial-data-sources.conf.j2
COPY resources/cloudbeaver/set_metadata.py /opt/cloudbeaver/set_metadata.py
COPY resources/cloudbeaver/set_metadata_run_jupyter.sh /set_metadata_run_jupyter.sh
RUN chmod +x /set_metadata_run_jupyter.sh
CMD ["/set_metadata_run_jupyter.sh"]

# Jupyterhub version
FROM --platform=linux/amd64 jupyter/minimal-notebook:python-3.8.13 as jupyterhub

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

# logos
COPY resources/logos/ /opt/logos/

# jupyter config
COPY resources/jupyter/jupyterhub/ /var/tmp/jupyter/
RUN cat /var/tmp/jupyter/jupyter_server_config_append >> /etc/jupyter/jupyter_server_config.py

RUN curl -o /usr/bin/snowsql-1.2.24-linux_x86_64.bash https://sfc-repo.snowflakecomputing.com/snowsql/bootstrap/1.2/linux_x86_64/snowsql-1.2.24-linux_x86_64.bash && \
    chmod a+x /usr/bin
RUN SNOWSQL_DEST=/var/tmp/bin SNOWSQL_LOGIN_SHELL=/etc/bash.bashrc bash /usr/bin/snowsql-1.2.24-linux_x86_64.bash

RUN chown -R jovyan:users $HOME
USER jovyan

RUN pip install --no-cache-dir \
    jupyterlab==$(conda list -f jupyterlab --json | grep -oP '(?<=\"version\": \")[^\"]*') \
    jupyterlab-git \
    jupyterlab-lsp \
    jupyter-server-proxy
RUN pip install --no-cache-dir data-pipelines-cli[docker,datahub,s3,snowflake]==${DP_CLI_VERSION}

# code server
COPY resources/vsc/addons/snowflake.snowflake-vsc-0.5.1.vsix /var/tmp
RUN curl -fsSL https://code-server.dev/install.sh | sh -s -- --version ${VSCODE_VERSION}
RUN code-server --extensions-dir /var/tmp/extension --install-extension ms-python.python \
    code-server --extensions-dir /var/tmp/extension --install-extension innoverio.vscode-dbt-power-user \
    code-server --extensions-dir /var/tmp/extension --install-extension /var/tmp/snowflake.snowflake-vsc-0.5.1.vsix


COPY resources/snowsql/config /var/tmp
CMD /var/tmp/bin/snowsql -v && \
    cp -f /var/tmp/config $HOME/.snowsql/ && \
    start-notebook.sh

