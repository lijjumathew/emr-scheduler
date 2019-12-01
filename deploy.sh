#!/bin/bash
set -e

# Check if required environment variables are set
: "${CLUSTER_NAME:?Need to set CLUSTER_NAME env variable}"
echo "CLUSTER_NAME: $CLUSTER_NAME"

: "${LOG_BUCKET:?Need to set LOG_BUCKET env variable}"
echo "LOG_BUCKET: $LOG_BUCKET"

: "${DEPLOYMENT_BUCKET:?Need to set DEPLOYMENT_BUCKET env variable}"
echo "DEPLOYMENT_BUCKET: $DEPLOYMENT_BUCKET"

: "${SUBNET_ID:?Need to set SUBNET_ID env variable}"
echo "SUBNET_ID: $SUBNET_ID"

# Zipping lambda function code
SERVICE_NAME=emr-scheduler
ROOT=$(pwd)
rm -rf target
mkdir target

echo Packing Start EMR Cluster Lambda Code
cd $ROOT/functions/start_emr_cluster
zip -9Dr  $ROOT/target/$SERVICE_NAME-start-emr-cluster.zip * -x *.pyc tests/* 

echo Packing Stop EMR Cluster Lambda Code
cd $ROOT/functions/stop_emr_cluster
zip -9Dr  $ROOT/target/$SERVICE_NAME-stop-emr-cluster.zip * -x *.pyc tests/* 

cd $ROOT
export SLS_DEBUG=true
echo Deploying serverless.yml
serverless deploy -v
echo Deployment Done