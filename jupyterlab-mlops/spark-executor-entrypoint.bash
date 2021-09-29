#!/bin/bash
DRIVER=`echo $SPARK_DRIVER_URL | cut -d@ -f 2`
echo "Checking Spark driver connectivity: $DRIVER"
SOCKET=/dev/tcp/`echo $DRIVER | tr : /`

while ! timeout 1 bash -c "echo > $SOCKET"; do
  echo "Driver not reachable, retrying in 1 second..."
  sleep 1
done

echo "Running Spark executor"
exec /usr/local/spark-3.1.2-bin-hadoop3.2/kubernetes/dockerfiles/spark/entrypoint.sh executor
