FROM dbeaver/cloudbeaver:22.0.5 AS builder-dbeaver
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
COPY resources/vsc/settings.json "/home/jupyter/.vscode/settings.json"
COPY resources/vsc/.bashrc "root/.bashrc"

# dbeaver
COPY --from=builder-dbeaver /opt/cloudbeaver/ /opt/cloudbeaver/
COPY resources/cloudbeaver/conf /opt/cloudbeaver/conf

# requirements
COPY requirements/requirements.txt /opt/requirements/
RUN pip install -r /opt/requirements/requirements.txt

# logos
COPY resources/logos/ /opt/logos/

# jupyter config
COPY resources/jupyter/ /etc/jupyter/

# Expose port for Vertex AI compatibility
EXPOSE 8080

FROM base as bigquery
COPY requirements/requirements-bigquery.txt /opt/requirements/
RUN pip install -r /opt/requirements/requirements-bigquery.txt