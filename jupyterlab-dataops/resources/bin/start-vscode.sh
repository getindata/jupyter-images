#!/bin/bash
/opt/code-server-*-linux-amd64/bin/code-server \
  --extensions-dir /tmp/jovyan/code-server/extensions \
  --user-data-dir /tmp/jovyan/code-server/data \
  --config /tmp/jovyan/code-server/config.yaml \
  --auth none --bind-addr 0.0.0.0:7000 \
  --disable-update-check --disable-telemetry -vvv
