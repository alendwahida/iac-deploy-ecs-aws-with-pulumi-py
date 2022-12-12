import json
import pulumi
import pulumi_aws as aws
import vars.varProjectDev as var

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