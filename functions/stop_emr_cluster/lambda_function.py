import boto3
import os
from datetime import datetime

EMR_CLIENT = boto3.client('emr')
CLUSTER_NAME = os.env('CLUSTER_NAME')


def lambda_handler(event, context):
    """ Lambda entry point"""

    cluster_exist_flag, cluster_id = check_emr_cluster()
    if cluster_exist_flag:
        print('Cluster already exists, stopping it')
        stop_emr_cluster(cluster_id)
    else:
        print('There is no cluster running')


def check_emr_cluster():

    exists_flag = False
    cluster_id = None
    response = EMR_CLIENT.list_clusters(
        CreatedAfter=datetime(2019, 4, 4),
        ClusterStates=['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING'],
    )

    for cluster in response['Clusters']:
        if cluster['Name'] == CLUSTER_NAME:
            exists_flag = True
            cluster_id = cluster['Id']

    return exists_flag, cluster_id


def stop_emr_cluster(cluster_id):

    EMR_CLIENT.terminate_job_flows(
        JobFlowIds=[cluster_id]
    )

    print('Stopping EMR Cluster - ' + cluster_id)
