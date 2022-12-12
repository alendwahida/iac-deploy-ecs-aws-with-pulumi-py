import json
import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx
import networking.vpcDev as vpcdev
import vars.projects as var
import routing.elbDev as elbdev
from pulumi import Output
from datetime import datetime

##########################################################################
# Project ECS Cluster Initialize
cluster=aws.ecs.Cluster(
    var.PROJECT_ECS_NAME,
    name=var.PROJECT_ECS_NAME,
    settings=[
        aws.ecs.ClusterSettingArgs(
            name="containerInsights",
            value="disabled"
        )
    ],
    tags={
        "Name": "ecs-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
 )

##########################################################################
# Project Tutum
task_definition_tutum_dev = aws.ecs.TaskDefinition(
    var.ECS_PROJECT_TUTUM+"-task-dev",
    family=var.ECS_PROJECT_TUTUM+"-task-definition",
    cpu=var.ECS_TASK_CPU_TUTUM,
    memory=var.ECS_TASK_MEM_TUTUM,
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=elbdev.role.arn,
    container_definitions=json.dumps([{
        "name": var.ECS_PROJECT_TUTUM+"-dev",
        "image": var.ECS_IMAGE_TUTUM,
        "portMappings": [{
            "containerPort": var.ECS_CONTAINER_PORT_TUTUM,
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
    name=var.ECS_PROJECT_TUTUM+"-svc-dev",
    desired_count=var.ECS_SVC_DESIRED_TASK_TUTUM,
    launch_type="FARGATE",
    task_definition=task_definition_tutum_dev.arn,
    network_configuration={
        "assign_public_ip": "true",
        "subnets": [vpcdev.subnetPublicA.id ,vpcdev.subnetPublicB.id],
        "security_groups": [elbdev.group.id]
    },
    load_balancers=[{
        "target_group_arn": elbdev.tg_tutum.arn,
        "container_name": var.ECS_PROJECT_TUTUM+"-dev",
        "container_port": var.ECS_CONTAINER_PORT_TUTUM
    }],
    opts=pulumi.ResourceOptions(depends_on=[elbdev.listenerhttp,elbdev.listenerhttps]),
    tags={
        "Name": "svc-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

ecs_target_tutum_dev=aws.appautoscaling.Target(
    var.ECS_PROJECT_TUTUM+"-ecs-target-dev",
    max_capacity=4,
    min_capacity=1,
    resource_id=Output.all(cluster.name,service_tutum_dev.name).apply(lambda args: f"service/{args[0]}/{args[1]}"),
    scalable_dimension="ecs:service:DesiredCount",
    service_namespace="ecs"
)

# Memory util policy
ecs_policy_memory_tutum_dev=aws.appautoscaling.Policy(
    var.ECS_PROJECT_TUTUM+"-mem-ecs-policy-dev",
    name=var.ECS_PROJECT_TUTUM+"-mem-ecs-policy-dev",
    policy_type="TargetTrackingScaling",
    resource_id=ecs_target_tutum_dev.resource_id,
    scalable_dimension=ecs_target_tutum_dev.scalable_dimension,
    service_namespace=ecs_target_tutum_dev.service_namespace,
    target_tracking_scaling_policy_configuration=aws.appautoscaling.PolicyTargetTrackingScalingPolicyConfigurationArgs(
        predefined_metric_specification=aws.appautoscaling.PolicyTargetTrackingScalingPolicyConfigurationPredefinedMetricSpecificationArgs(
            predefined_metric_type="ECSServiceAverageMemoryUtilization"
        ),
        target_value=60,
        scale_in_cooldown=100,  # in seconds
        scale_out_cooldown=20   # in seconds
    )
)

##########################################################################
# Project Nginx
task_definition_nginx_dev = aws.ecs.TaskDefinition(
    var.ECS_PROJECT_NGINX+"-task-dev",
    family=var.ECS_PROJECT_NGINX+"-task-definition",
    cpu=var.ECS_TASK_CPU_NGINX,
    memory=var.ECS_TASK_MEM_NGINX,
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=elbdev.role.arn,
    container_definitions=json.dumps([{
        "name": var.ECS_PROJECT_NGINX+"-dev",
        "image": var.ECS_IMAGE_NGINX,
        "portMappings": [{
            "containerPort": var.ECS_CONTAINER_PORT_NGINX,
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
    name=var.ECS_PROJECT_NGINX+"-svc-dev",
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
        "container_port": var.ECS_CONTAINER_PORT_NGINX
    }],
    opts=pulumi.ResourceOptions(depends_on=[elbdev.listenerhttp,elbdev.listenerhttps]),
    tags={
        "Name": "svc-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

ecs_target_nginx_dev=aws.appautoscaling.Target(
    var.ECS_PROJECT_NGINX+"-ecs-target-dev",
    max_capacity=4,
    min_capacity=1,
    resource_id=Output.all(cluster.name,service_nginx_dev.name).apply(lambda args: f"service/{args[0]}/{args[1]}"),
    scalable_dimension="ecs:service:DesiredCount",
    service_namespace="ecs"
)
# Memory util policy
ecs_policy_memory_nginx_dev=aws.appautoscaling.Policy(
    var.ECS_PROJECT_NGINX+"-mem-ecs-policy-dev",
    name=var.ECS_PROJECT_NGINX+"-mem-ecs-policy-dev",
    policy_type="TargetTrackingScaling",
    resource_id=ecs_target_nginx_dev.resource_id,
    scalable_dimension=ecs_target_nginx_dev.scalable_dimension,
    service_namespace=ecs_target_nginx_dev.service_namespace,
    target_tracking_scaling_policy_configuration=aws.appautoscaling.PolicyTargetTrackingScalingPolicyConfigurationArgs(
        predefined_metric_specification=aws.appautoscaling.PolicyTargetTrackingScalingPolicyConfigurationPredefinedMetricSpecificationArgs(
            predefined_metric_type="ECSServiceAverageMemoryUtilization"
        ),
        target_value=60,
        scale_in_cooldown=100,  # in seconds
        scale_out_cooldown=20   # in seconds
    )
)

# CPU util policy
ecs_policy_cpu_nginx_dev=aws.appautoscaling.Policy(
    var.ECS_PROJECT_NGINX+"-cpu-ecs-policy-dev",
    name=var.ECS_PROJECT_NGINX+"-cpu-ecs-policy-dev",
    policy_type="TargetTrackingScaling",
    resource_id=ecs_target_nginx_dev.resource_id,
    scalable_dimension=ecs_target_nginx_dev.scalable_dimension,
    service_namespace=ecs_target_nginx_dev.service_namespace,
    target_tracking_scaling_policy_configuration=aws.appautoscaling.PolicyTargetTrackingScalingPolicyConfigurationArgs(
        predefined_metric_specification=aws.appautoscaling.PolicyTargetTrackingScalingPolicyConfigurationPredefinedMetricSpecificationArgs(
            predefined_metric_type="ECSServiceAverageCPUUtilization"
        ),
        target_value=80,
        scale_in_cooldown=100,  # in seconds
        scale_out_cooldown=20   # in seconds
    )
)