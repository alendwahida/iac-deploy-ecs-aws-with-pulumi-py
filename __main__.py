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

task_definition_webapp_dev = aws.ecs.TaskDefinition(
    "webapp-task-dev",
    family="fargate-task-definition",
    cpu="256",
    memory="512",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=elbdev.role.arn,
    container_definitions=json.dumps([{
        "name": "webapp-dev",
        "image": var.ECS_IMAGE,
        "portMappings": [{
            "containerPort": var.ECS_CONTAINER_PORT,
            "hostPort": 80,
            "protocol": "tcp"
        }]
    }]),
    tags={
        "Name": "task-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

service_webapp_dev = aws.ecs.Service(
    "webapp-svc-dev",
    cluster=cluster.arn,
    desired_count=var.ECS_SVC_DESIRED_TASK,
    launch_type="FARGATE",
    task_definition=task_definition_webapp_dev.arn,
    network_configuration={
        "assign_public_ip": "true",
        "subnets": [vpcdev.subnetPublicA.id ,vpcdev.subnetPublicB.id],
        "security_groups": [elbdev.group.id]
    },
    load_balancers=[{
        "target_group_arn": elbdev.target_group.arn,
        "container_name": "webapp-dev",
        "container_port": var.ECS_CONTAINER_PORT
    }],
    opts=pulumi.ResourceOptions(depends_on=[elbdev.listenerhttp,elbdev.listenerhttps]),
    tags={
        "Name": "svc-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)