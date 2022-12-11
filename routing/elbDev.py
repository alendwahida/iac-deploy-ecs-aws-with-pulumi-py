import json
import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx

import networking.vpcDev as vpcdev
import vars.projects as var

###########################################################################
# SecurityGroup
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

###########################################################################
# Setup Loadbalancer
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

###########################################################################
# Webapp target Group
tg_tutum=aws.lb.TargetGroup(
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
# Nginx target Group
tg_nginx=aws.lb.TargetGroup(
    "tg-nginx-dev",
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

###########################################################################
# Setup Default Listener
listenerhttp=aws.lb.Listener(
    "http-dev",
    load_balancer_arn=alb.arn,
    port=80,
    protocol="HTTP",
    default_actions=[
        aws.lb.ListenerDefaultActionArgs(
            type="fixed-response",
            fixed_response=aws.lb.ListenerDefaultActionFixedResponseArgs(
                content_type="text/plain",
                message_body="HTTP",
                status_code="200"
            )
        )
    ],
    tags={
        "Name": "lb-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

listenerhttps=aws.lb.Listener(
    "https-dev",
    load_balancer_arn=alb.arn,
    port=443,
    protocol="HTTPS",
    ssl_policy="ELBSecurityPolicy-2016-08",
    certificate_arn=var.LB_SSL_ARN_DEV,
    default_actions=[
        aws.lb.ListenerDefaultActionArgs(
            type="fixed-response",
            fixed_response=aws.lb.ListenerDefaultActionFixedResponseArgs(
                content_type="text/plain",
                message_body="HTTPS",
                status_code="200"
            )
        )
    ],
    tags={
        "Name": "lb-"+var.PROJECT_ECS_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)
###########################################################################
# Listener Rules for Webapp
listenerRuleHttps_webapp=aws.lb.ListenerRule(
    "listenerRuleHttpsTutum",
    listener_arn=listenerhttps.arn,
    actions=[aws.lb.ListenerRuleActionArgs(
        type="forward",
        target_group_arn=tg_tutum.arn
    )],
    conditions=[
        aws.lb.ListenerRuleConditionArgs(
            host_header=aws.lb.ListenerRuleConditionHostHeaderArgs(
                values=[var.LB_HOST_TUTUM_DEV]
            )
        )
    ]
)
# Listener Rules for Nginx
listenerRuleHttps_nginx=aws.lb.ListenerRule(
    "listenerRuleHttpsNginx",
    listener_arn=listenerhttps.arn,
    actions=[aws.lb.ListenerRuleActionArgs(
        type="forward",
        target_group_arn=tg_nginx.arn
    )],
    conditions=[
        aws.lb.ListenerRuleConditionArgs(
            host_header=aws.lb.ListenerRuleConditionHostHeaderArgs(
                values=[var.LB_HOST_NGINX_DEV]
            )
        )
    ]
)

##########################################################################
# Iam Role for ELB - ECS Fargate
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