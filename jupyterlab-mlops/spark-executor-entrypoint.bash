#!/bin/bash
DRIVER=`echo $SPARK_DRIVER_URL | cut -d@ -f 2`
echo "Checking Spark driver connectivity: $DRIVER"
SOCKET=/dev/tcp/`echo $DRIVER | tr : /`

while ! timeout 1 bash -c "echo > $SOCKET"; do
  echo "Driver not reachable, retrying in 1 second..."
  sleep 1
done

echo "Running Spark executor"
/usr/local/spark-3.1.2-bin-hadoop3.2/kubernetes/dockerfiles/spark/entrypoint.sh executor
EXIT_CODE=$?

echo "Stopping istio-proxy (if enabled)"
curl --max-time 2 -s -f -XPOST http://127.0.0.1:15000/quitquitquit

exit $EXIT_CODE
