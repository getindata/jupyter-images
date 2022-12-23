#!/bin/bash
set -e
mkdir -p /home/jovyan/.snowsql
cp /var/tmp/config /home/jovyan/.snowsql/config
cp /var/tmp/settings.json /home/jovyan/.vscode/settings.json
chown jovyan:users -R /home/jovyan/.snowsql
start-notebook.sh
