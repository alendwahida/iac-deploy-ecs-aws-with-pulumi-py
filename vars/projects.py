import os

PROJECT_NETWORK_NAME="NetworkingDev"
PROJECT_ENVIRONMENT="Development"
PROJECT_COST_NAME="AWS"
PROJECT_ECS_NAME="ECSinDev"

# ECS Task Settings
ECS_IMAGE="nginx:latest"
ECS_CONTAINER_PORT=80

# ECS Service Settings
ECS_SVC_DESIRED_TASK=3

# ELB Settings
LB_SSL_ARN_DEV="arn:aws:acm:us-east-1:0123456789:certificate/xxxxx-xxxx-xxxx-xxxxx"
LB_HOST_TEST_DEV="test.xxx.com"