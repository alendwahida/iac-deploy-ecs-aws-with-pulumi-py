import os

PROJECT_NETWORK_NAME="NetworkingDev"
PROJECT_ENVIRONMENT="Development"
PROJECT_COST_NAME="AWS"
PROJECT_ECS_NAME="ECS-Dev"

# ECS Task-Service Tutum Settings
ECS_PROJECT_TUTUM="ProjectTutum"
ECS_IMAGE_TUTUM="tutum/hello-world:latest"
ECS_CONTAINER_PORT_TUTUM=80
ECS_SVC_DESIRED_TASK_TUTUM=2

# ECS Task-Service Nginx Settings
ECS_PROJECT_NGINX="ProjectNginx"
ECS_IMAGE_NGINX="nginx:latest"
ECS_CONTAINER_PORT=80
ECS_SVC_DESIRED_TASK_NGINX=1

# ELB Setting Domain
LB_SSL_ARN_DEV=os.getenv("ARN_SSL_FOR_FARGATE") # arn certificate manager aws
LB_HOST_TUTUM_DEV=os.getenv("WWW_TUTUM") # www.tutum.example.com
LB_HOST_NGINX_DEV=os.getenv("WWW_NGINX") # www.nginx.example.com