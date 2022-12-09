import json
import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

import networking.vpcDev as vpcdev
import vars.projects as var

group=aws.ec2.SecurityGroup(
    "secgroup-webapp-dev",
    vpc_id=vpcdev.infradev.id,
    description="HTTP and HTTPS Access Dev",
    ingress=[aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=80,
        to_port=80,
        cidr_blocks=["0.0.0.0/0"]
    ),aws.ec2.SecurityGroupIngressArgs(
        protocol="tcp",
        from_port=443,
        to_port=443,
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

listenerhttp=aws.lb.Listener(
    "webapp-http-dev",
    load_balancer_arn=alb.arn,
    port=80,
    protocol="HTTP",
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

listenerhttps=aws.lb.Listener(
    "webapp-https-dev",
    load_balancer_arn=alb.arn,
    port=443,
    protocol="HTTPS",
    ssl_policy="ELBSecurityPolicy-2016-08",
    certificate_arn=var.LB_SSL_ARN_DEV,
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

listenerRuleHttps=aws.lb.ListenerRule(
    "listenerRuleHttps",
    listener_arn=listenerhttps.arn,
    priority=1,
    actions=[aws.lb.ListenerRuleActionArgs(
        type="forward",
        target_group_arn=target_group.arn
    )],
    conditions=[
        aws.lb.ListenerRuleConditionArgs(
            host_header=aws.lb.ListenerRuleConditionHostHeaderArgs(
                values=[var.LB_HOST_TEST_DEV]
            )
        )
    ]
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