import json
import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

import networking.vpcDev as vpcdev
import vars.projects as var

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

group=aws.ec2.SecurityGroup(
    "secgroup-webapp-dev",
    vpc_id=vpcdev.infradev.id,
    description="HTTP Access Dev",
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=80,
        to_port=80,
        cidr_blocks=["0.0.0.0/0"]
    )],
    egress=[aws.ec2.SecurityGroupIngressArgs(
        protocol="-1",
        from_port=0,
        to_port=0,
        cidr_blocks=["0.0.0.0/0"]
    )],
    tags={
        "Name": "secgroup-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

alb=aws.lb.LoadBalancer(
    "lb-webapp-dev",
    security_groups=[group.id],
    subnets=[vpcdev.subnetPublicA.id,vpcdev.subnetPublicB.id],
    tags={
        "Name": "elb-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

target_group=aws.lb.TargetGroup(
    "tg-webapp-dev",
    port=80,
    protocol="HTTP",
    target_type="ip",
    vpc_id=vpcdev.infradev.id,
    tags={
        "Name": "tg-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

listener=aws.lb.Listener(
    "webapp-dev",
    load_balancer_arn=alb.arn,
    port=80,
    default_actions=[
        aws.lb.ListenerDefaultActionArgs(
            type="forward",
            target_group_arn=target_group.arn
        )
    ],
    tags={
        "Name": "lb-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

role=aws.iam.Role(
    "task-exec-role-dev",
    assume_role_policy=json.dumps({
        "Version": "2008-10-17",
        "Statement": [{
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
                "Service": "ecs-tasks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }]
    }),
    tags={
        "Name": "role-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

aws.iam.RolePolicyAttachment(
    "task-exec-policy-dev",
    role=role.name,
    policy_arn="arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
)

task_definition = aws.ecs.TaskDefinition(
    "webapp-task-dev",
    family="fargate-task-definition",
    cpu="256",
    memory="512",
    network_mode="awsvpc",
    requires_compatibilities=["FARGATE"],
    execution_role_arn=role.arn,
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

service = aws.ecs.Service(
    "webapp-svc-dev",
    cluster=cluster.arn,
    desired_count=var.ECS_SVC_DESIRED_TASK,
    launch_type="FARGATE",
    task_definition=task_definition.arn,
    network_configuration={
        "assign_public_ip": "true",
        "subnets": [vpcdev.subnetPublicA.id ,vpcdev.subnetPublicB.id],
        "security_groups": [group.id]
    },
    load_balancers=[{
        "target_group_arn": target_group.arn,
        "container_name": "webapp-dev",
        "container_port": var.ECS_CONTAINER_PORT
    }],
    opts=pulumi.ResourceOptions(depends_on=[listener]),
    tags={
        "Name": "svc-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

pulumi.export("url", pulumi.Output.concat("http://", alb.dns_name))