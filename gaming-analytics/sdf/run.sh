# fluvio cluster start
# fluvio cluster status
# cd /workspace/connectors/
# cdk deploy start --ipkg infinyon-http-source-0.4.3.ipkg -c license-connector.yaml
# cdk deploy start --ipkg infinyon-http-source-0.4.3.ipkg -c car-connector.yaml
# cd /workspace
set -e

sdf clean

echo Starting Worker
sdf worker create compose-service --worker-id compose-service

echo Starting SDF Deploy
sdf deploy --ui
