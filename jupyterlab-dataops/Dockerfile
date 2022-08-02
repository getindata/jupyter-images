# FROM dbeaver/cloudbeaver:22.0.5 AS builder-dbeaver
FROM gcr.io/deeplearning-platform-release/base-cpu:m88
RUN apt-get update && apt-get install -yq --no-install-recommends \
    curl \
    git \
    # openjdk-11-jdk \
    && apt-get clean && rm -rf /var/lib/apt/lists/*
# code-server install
RUN curl -fsSL https://code-server.dev/install.sh | sh && \
    rm -rf "${HOME}/.cache"

# COPY --from=builder-dbeaver /opt/cloudbeaver/ /opt/cloudbeaver/
# COPY resources/cloudbeaver/conf /opt/cloudbeaver/conf
COPY requirements/ /opt/requirements/
RUN pip install -r /opt/requirements/requirements.txt
COPY resources/jupyter/ /etc/jupyter/
COPY resources/logos/ /opt/logos/

COPY resources/vsc/vsix/ /opt/vsix/
RUN code-server --install-extension ms-python.python \
    code-server --install-extension /opt/vsix/innoverio.vscode-dbt-power-user-0.5.9.vsix \
    code-server --install-extension /opt/vsix/bastienboutonnet.vscode-dbt-0.5.1.vsix
COPY resources/vsc/settings.json "/home/jupyter/.local/share/code-server/User/settings.json"

EXPOSE 8080