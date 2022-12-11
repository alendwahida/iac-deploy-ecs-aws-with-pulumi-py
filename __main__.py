import json
import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

import networking.vpcDev as vpcdev
import vars.projects as var
import routing.elbDev as elbdev

cluster=aws.ecs.Cluster(
    "DevCluster",
    settings=[
        aws.ecs.ClusterSettingArgs(
            name="containerInsights",
            value="enabled"
        )
    ],
    tags={
        "Name": "ecs"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
 )

##########################################################################
# Project Tutum
task_definition_tutum_dev = aws.ecs.TaskDefinition(
    var.ECS_PROJECT_TUTUM+"-task-dev",
    family=var.ECS_PROJECT_TUTUM+"-task-definition",
    cpu="256",
    memory="512",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=elbdev.role.arn,
    container_definitions=json.dumps([{
        "name": var.ECS_PROJECT_TUTUM+"-dev",
        "image": var.ECS_IMAGE_TUTUM,
        "portMappings": [{
            "containerPort": var.ECS_CONTAINER_PORT,
            "hostPort": 80,
            "protocol": "tcp"
        }],
        "environment": [{
            "name": "USERNAME",
            "value" : "USERUSER"

        },{
            "name": "PASSWORD",
            "value": "PASSWORD"
        }]
    }]),
    tags={
        "Name": "task-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

service_tutum_dev = aws.ecs.Service(
    var.ECS_PROJECT_TUTUM+"-svc-dev",
    cluster=cluster.arn,
    desired_count=var.ECS_SVC_DESIRED_TASK_TUTUM,
    launch_type="FARGATE",
    task_definition=task_definition_tutum_dev.arn,
    network_configuration={
        "assign_public_ip": "true",
        "subnets": [vpcdev.subnetPublicA.id ,vpcdev.subnetPublicB.id],
        "security_groups": [elbdev.group.id]
    },
    load_balancers=[{
        "target_group_arn": elbdev.tg_webapp.arn,
        "container_name": var.ECS_PROJECT_TUTUM+"-dev",
        "container_port": var.ECS_CONTAINER_PORT
    }],
    opts=pulumi.ResourceOptions(depends_on=[elbdev.listenerhttp,elbdev.listenerhttps]),
    tags={
        "Name": "svc-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

##########################################################################
# Project Nginx
task_definition_nginx_dev = aws.ecs.TaskDefinition(
    var.ECS_PROJECT_NGINX+"-task-dev",
    family=var.ECS_PROJECT_NGINX+"-task-definition",
    cpu="256",
    memory="512",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=elbdev.role.arn,
    container_definitions=json.dumps([{
        "name": var.ECS_PROJECT_NGINX+"-dev",
        "image": var.ECS_IMAGE_NGINX,
        "portMappings": [{
            "containerPort": var.ECS_CONTAINER_PORT,
            "hostPort": 80,
            "protocol": "tcp"
        }],
        "environment": [{
            "name": "USERNAME",
            "value" : "USERUSER"

        }]
    }]),
    tags={
        "Name": "task-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

service_nginx_dev = aws.ecs.Service(
    var.ECS_PROJECT_NGINX+"-svc-dev",
    cluster=cluster.arn,
    desired_count=var.ECS_SVC_DESIRED_TASK_NGINX,
    launch_type="FARGATE",
    task_definition=task_definition_nginx_dev.arn,
    network_configuration={
        "assign_public_ip": "true",
        "subnets": [vpcdev.subnetPublicA.id ,vpcdev.subnetPublicB.id],
        "security_groups": [elbdev.group.id]
    },
    load_balancers=[{
        "target_group_arn": elbdev.tg_nginx.arn,
        "container_name": var.ECS_PROJECT_NGINX+"-dev",
        "container_port": var.ECS_CONTAINER_PORT
    }],
    opts=pulumi.ResourceOptions(depends_on=[elbdev.listenerhttp,elbdev.listenerhttps]),
    tags={
        "Name": "svc-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)