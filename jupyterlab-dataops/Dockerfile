FROM gcr.io/deeplearning-platform-release/base-cpu:m88 as base

ARG VSCODE_VERSION=4.5.1
ARG VSCODE_PYTHON=2022.13.12141005
ARG VSCODE_DBT_POWER_USER=0.6.2
ARG VSCODE_DBT=0.5.1

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
RUN code-server --install-extension ms-python.python@${VSCODE_PYTHON} \
    code-server --install-extension innoverio.vscode-dbt-power-user@${VSCODE_DBT_POWER_USER} \
    code-server --install-extension bastienboutonnet.vscode-dbt@${VSCODE_DBT}
COPY resources/vsc/settings.json /root/.local/share/code-server/Machine/
COPY resources/vsc/.bashrc root/

# cloudbeaver
COPY --from=gcr.io/getindata-images-public/cloudbeaver-dataops /opt/cloudbeaver/ /opt/cloudbeaver/

# requirements
COPY requirements/requirements.txt /opt/requirements/
RUN pip install -r /opt/requirements/requirements.txt

# logos
COPY resources/logos/ /opt/logos/

# jupyter config
COPY resources/jupyter/ /etc/jupyter/

# Expose port for Vertex AI compatibility
EXPOSE 8080

# use default cloudbeaver in non-bigquery target
FROM base AS default
COPY resources/cloudbeaver/conf /opt/cloudbeaver/conf

FROM base as bigquery
COPY requirements/requirements-bigquery.txt /opt/requirements/
RUN pip install -r /opt/requirements/requirements-bigquery.txt
COPY --from=gcr.io/getindata-images-public/cloudbeaver-dataops /opt/cloudbeaver/ /opt/cloudbeaver/
COPY resources/cloudbeaver/conf /opt/cloudbeaver/conf
ADD resources/cloudbeaver/conf/initial-data-sources-bigquery.conf /opt/cloudbeaver/conf/initial-data-sources.conf
COPY resources/cloudbeaver/set_metadata.py /opt/cloudbeaver/set_metadata.py
COPY resources/cloudbeaver/set_metadata_run_jupyter.sh /set_metadata_run_jupyter.sh
RUN chmod +x /set_metadata_run_jupyter.sh
CMD ["/set_metadata_run_jupyter.sh"]
