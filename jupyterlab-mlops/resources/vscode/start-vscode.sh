#!/bin/bash
/opt/code-server/bin/code-server \
  --auth none --bind-addr 0.0.0.0:7000 \
  --disable-update-check --disable-telemetry -vvv