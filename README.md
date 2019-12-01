### Intro
1. This repo consists of artifacts to schedule emr clusters
2. It has two lambda's one to start the emr cluster and other to stop the emr cluster
3. When to start and stop the cluster can be adjusted as per the need, it is a cron schedule.
4. The assumptions is that emr cluster runs in a public subnet, if the emr cluster runs in private subnet then lambdas
   need to run in private subnet
5. Built using serverless framework

### Prerequisites
Install latest version of
1. npm
2. node
3. serverless
4. aws cli (aslo, configure the cli with credentials)

Also have the below variables set 

`export DEV=<Environment name like dev,qa,test etc>   
export CLUSTER_NAME=<Name of the Cluster>   
export LOG_BUCKET=<S3 Bucket name for logs, should be created before deploying>   
export DEPLOYMENT_BUCKET=<S3 Bucket name for deployments, should be created before deploying>   
export SUBNET_ID=<Subnet id where EMR Cluster should run>   
`

### Deployment
1. Clone the repo
2. From the base folder and bash prompt run 
   sh deploy.sh