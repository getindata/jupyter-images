ARG BASE_IMAGE=jupyter/base-notebook:python-3.8.8
FROM $BASE_IMAGE

USER root
ARG PIP_VERSION=21.0.1
ARG USER_NAME=jovyan
ARG PROVIDER=""
ENV HOME=/tmp/$USER_NAME

ADD resources/bin/*.sh /opt/tools/bin/
ADD resources/logos/* /opt/tools/logos/
ADD resources/config/jupyter_notebook_config.py resources/config/jupyter_server_config.py  /etc/jupyter/
ADD resources/vsc/vsix/* /tmp/$NB_USER/vsix/
# Copy `requirements.txt` and `requirements-${PROVIDER}.txt`, if exists.
COPY requirements.txt requirements-${PROVIDER}.tx[t] $HOME/

RUN apt-get update --fix-missing && apt-get -qq -y install \
    curl 
#     gnupg2

# RUN sh -c 'curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add - && \
#     echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list && \
#     curl -sL https://deb.nodesource.com/setup_16.x | sudo -E bash -'

RUN apt-get update --fix-missing && apt-get -qq -y install \
    unzip \
    zip \
    jq \
    git && \
    # openjdk-11-jdk \
    # maven \
    # yarn \
    # nodejs && \
    rm /bin/sh && ln -s /bin/bash /bin/sh

# # Cloudbeaver needs newer node
# RUN ln -sf /bin/node /opt/conda/bin/node
# RUN ln -sf /bin/npm /opt/conda/bin/npm

# RUN npm install -g lerna

# # Clone cloudbeaver
# RUN git clone https://github.com/dbeaver/cloudbeaver.git /tmp/cloudbeaver && \
#     cd /tmp/cloudbeaver

# # Add BigQuery drivers
# RUN if [[ $PROVIDER == "bigquery" ]] ; then mkdir -p /tmp/cloudbeaver/server/drivers/bigquery/src/main/resources && \
#     wget https://storage.googleapis.com/simba-bq-release/jdbc/SimbaJDBCDriverforGoogleBigQuery42_1.2.16.1020.zip && \
#     unzip SimbaJDBCDriverforGoogleBigQuery42_1.2.16.1020.zip -d /tmp/cloudbeaver/server/drivers/bigquery/src/main/resources && \
#     rm SimbaJDBCDriverforGoogleBigQuery42_1.2.16.1020.zip ; fi
# ADD resources/cloudbeaver/plugin-${PROVIDER:-default}.xm[l] /tmp/cloudbeaver/server/bundles/io.cloudbeaver.resources.drivers.base/plugin.xml
# ADD resources/cloudbeaver/drivers/pom-${PROVIDER:-default}.xm[l] /tmp/cloudbeaver/server/drivers/pom.xml
# ADD resources/cloudbeaver/drivers/${PROVIDER}/pom.xm[l] /tmp/cloudbeaver/server/drivers/bigquery/pom.xml

# Build
# RUN cd /tmp/cloudbeaver/deploy && ./build.sh "" ""

RUN mkdir -p $HOME && chown -R $USER_NAME $HOME && \
    mkdir -p /opt/tools/{bin,logos} && \
    chmod -R 755 /opt/tools/ && \
    mkdir -p /mnt/data && chown -R $NB_USER /mnt/data

# Install Python and Jupyter extensions
RUN pip install -r $HOME/requirements.txt
RUN if [[ -z "$PROVIDER" ]] ; then echo "Argument PROVIDER not provided" ; else pip install -r $HOME/requirements-${PROVIDER}.txt ; fi
RUN jupyter labextension install @jupyterlab/server-proxy jupyterlab-topbar-extension

# Install code server
RUN cd /opt/ && wget https://github.com/cdr/code-server/releases/download/v4.3.0/code-server-4.3.0-linux-amd64.tar.gz && \
    tar zxvf code-server-4.3.0-linux-amd64.tar.gz

# # Copy Cloudbeaver
# RUN mv /tmp/cloudbeaver/deploy/cloudbeaver /opt/tools/cloudbeaver
# RUN mkdir -p /opt/tools/cloudbeaver/workspace && chmod -R 755 /opt/tools && chmod a+rwX -R /opt/tools/cloudbeaver/workspace

USER $NB_USER
RUN /opt/code-server-*-linux-amd64/bin/code-server \
    --extensions-dir $HOME/code-server/extensions \
    --user-data-dir $HOME/code-server/data \
    --config $HOME/code-server/config.yaml \
    --install-extension ms-python.python \
    /opt/code-server-*-linux-amd64/bin/code-server \
    --install-extension /tmp/$NB_USER/vsix/innoverio.vscode-dbt-power-user-0.5.16.vsix \
    /opt/code-server-*-linux-amd64/bin/code-server \
    --install-extension /tmp/$NB_USER/vsix/bastienboutonnet.vscode-dbt-0.5.1.vsix

ADD resources/vsc/settings.json $HOME/code-server/data/User/settings.json

# COPY resources/cloudbeaver/conf /opt/tools/cloudbeaver/conf
# ADD resources/cloudbeaver/conf/.cloudbeaver.auto.conf /opt/tools/cloudbeaver/conf/.cloudbeaver.auto.conf
# ADD resources/cloudbeaver/conf/cloudbeaver.conf /opt/tools/cloudbeaver/conf/cloudbeaver.conf
# ADD resources/cloudbeaver/conf/initial-data-sources-${PROVIDER}.con[f] /opt/tools/cloudbeaver/conf/initial-data-sources.conf
# ADD resources/cloudbeaver/conf/product.conf /opt/tools/cloudbeaver/conf/product.conf

ENV HOME=/home/$USER_NAME
ENV CODE_WORKINGDIR="${HOME}/work"
ENV PATH="${PATH}:${CONDA_DIR}/envs/python38/bin"
ENV CONDA_DEFAULT_ENV=python38
ENV JUPYTER_ENABLE_LAB=yes
# Expose port for Vertex AI compatibility
EXPOSE 8080