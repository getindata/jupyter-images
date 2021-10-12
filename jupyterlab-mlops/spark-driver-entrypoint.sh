#!/bin/sh
exec /usr/local/spark-3.1.2-bin-hadoop3.2/kubernetes/dockerfiles/spark/entrypoint.sh driver "$@"
