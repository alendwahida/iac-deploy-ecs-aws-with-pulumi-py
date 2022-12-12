import pulumi
import pulumi_aws as aws
from datetime import datetime

config=pulumi.Config()

PROJECT_NAME="AlenoDev"

# Networking
PROJECT_NETWORK_NAME="NetworkingDev"

# ECS Tagging
PROJECT_ENVIRONMENT="Development"
PROJECT_COST_NAME="AWS"
PROJECT_ECS_NAME="ECS-Dev"

# ECS Task-Service Tutum Settings
ECS_PROJECT_TUTUM="ProjectTutum"
ECS_IMAGE_TUTUM="tutum/hello-world:latest"
ECS_CONTAINER_PORT_TUTUM=80
ECS_SVC_DESIRED_TASK_TUTUM=2
ECS_TASK_CPU_TUTUM="256"
ECS_TASK_MEM_TUTUM="512"

# ECS Task-Service Nginx Settings
ECS_PROJECT_NGINX="ProjectNginx"
ECS_IMAGE_NGINX="nginx:latest"
ECS_CONTAINER_PORT_NGINX=80
ECS_SVC_DESIRED_TASK_NGINX=1
ECS_TASK_CPU_NGINX="256"
ECS_TASK_MEM_NGINX="512"

# ELB Setting Domain
LB_SSL_ARN_DEV=config.require_secret('LB_SSL_ARN_DEV') # arn certificate manager aws
LB_HOST_TUTUM_DEV=config.require_secret('LB_HOST_TUTUM_DEV') # www.tutum.example.com
LB_HOST_NGINX_DEV=config.require_secret('LB_HOST_NGINX_DEV') # www.nginx.example.com