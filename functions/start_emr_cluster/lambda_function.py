import boto3
import os
from datetime import datetime

EMR_CLIENT = boto3.client('emr')
CLUSTER_NAME = os.getenv('CLUSTER_NAME')
LOG_BUCKET = os.getenv('LOG_BUCKET')
SUBNET_ID = os.getenv('SUBNET_ID')


def handler(event, context):
    """ Lambda entry point"""

    if check_emr_cluster():
        print('Cluster already exists')
    else:
        print('Calling create emr cluster')
        start_emr_cluster()


def check_emr_cluster():

    exists_flag = False
    response = EMR_CLIENT.list_clusters(
        CreatedAfter=datetime(2019, 4, 4),
        ClusterStates=['STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING'],
    )

    for cluster in response['Clusters']:
        if cluster['Name'] == CLUSTER_NAME:
            exists_flag = True

    return exists_flag


def start_emr_cluster():

    response = EMR_CLIENT.run_job_flow(
        Name=CLUSTER_NAME,
        LogUri='s3://' + LOG_BUCKET + '/emr_logs',
        ReleaseLabel='emr-5.23.0',
        Applications=[
            {
                'Name': 'Spark'
            },
            {
                'Name': 'Hadoop'
            },
            {
                'Name': 'Livy'
            }
        ],
        Configurations=[
            {
                'Classification': 'spark-env',
                'Configurations': [
                    {
                        "Classification": "export",
                        "Properties": {
                            "PYSPARK_PYTHON": "python3",
                            "PYSPARK_PYTHON_DRIVER": "python3"
                        }
                    }
                ]
            },
            {
                "Classification": "mapred-site",
                "Properties": {
                    "mapred.output.committer.class": "org.apache.hadoop.mapred.FileOutputCommitter",
                    "mapreduce.fileoutputcommitter.marksuccessfuljobs": "false",
                    "mapreduce.fileoutputcommitter.algorithm.version": "2",
                }
            }

        ],
        Instances={
            'InstanceGroups': [
                {
                    'Name': "Master nodes",
                    'Market': 'ON_DEMAND',
                    'InstanceRole': 'MASTER',
                    'InstanceType': 'm3.xlarge',
                    'InstanceCount': 1,
                },
                {
                    'Name': "Slave nodes",
                    'Market': 'ON_DEMAND',
                    'InstanceRole': 'CORE',
                    'InstanceType': 'm3.xlarge',
                    'InstanceCount': 2,
                }
            ],
            'Ec2KeyName': 'emrcluster',
            'KeepJobFlowAliveWhenNoSteps': True,
            'TerminationProtected': False,
            'Ec2SubnetId': SUBNET_ID
        },
        VisibleToAllUsers=True,
        JobFlowRole='EMR_EC2_DefaultRole',
        ServiceRole='EMR_DefaultRole',
    )

    print('Created a cluster with id :' + response['JobFlowId'])
