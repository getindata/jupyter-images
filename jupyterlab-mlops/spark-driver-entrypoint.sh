#!/bin/sh
exec /usr/local/spark-3.2.0-bin-hadoop3.2/kubernetes/dockerfiles/spark/entrypoint.sh driver "$@"
