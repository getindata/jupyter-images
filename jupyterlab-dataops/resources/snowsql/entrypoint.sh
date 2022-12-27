#!/bin/bash
set -e
mkdir -p /home/jovyan/.snowsql
mkdir -p /home/jovyan/.vscode
cp /var/tmp/config /home/jovyan/.snowsql/config
cp /var/tmp/settings.json /home/jovyan/.vscode/settings.json
cp /var/tmp/.bashrc /home/jovyan/.bashrc
chown jovyan:users -R /home/jovyan/.snowsql
chown jovyan:users -R /home/jovyan/.vscode
chown jovyan:users -R /home/jovyan/.bashrc
start-notebook.sh
