import pulumi
import pulumi_aws as aws

import vars.varProjectDev as var

infradev=aws.ec2.Vpc(
    "vpc-dev",
    cidr_block="10.0.0.0/16",
    instance_tenancy="default",
    enable_dns_hostnames=True,
    tags={
        "Name": "vpc-"+var.PROJECT_NETWORK_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

igwdev=aws.ec2.InternetGateway(
    "igw-dev",
    vpc_id=infradev.id,
    tags={
        "Name": "igw-"+var.PROJECT_NETWORK_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

subnetPublicA=aws.ec2.Subnet(
    "subnet-public-A",
    vpc_id=infradev.id,
    availability_zone="us-east-1a",
    map_public_ip_on_launch=True,
    cidr_block="10.0.1.0/24",
    tags={
        "Name": "subnet-public-a-"+var.PROJECT_NETWORK_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)
    
subnetPublicB=aws.ec2.Subnet(
    "subnet-public-B",
    vpc_id=infradev.id,
    availability_zone="us-east-1b",
    map_public_ip_on_launch=True,
    cidr_block="10.0.2.0/24",
    tags={
        "Name": "subnet-public-b-"+var.PROJECT_NETWORK_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

subnetPublicC=aws.ec2.Subnet(
    "subnet-public-C",
    vpc_id=infradev.id,
    availability_zone="us-east-1c",
    map_public_ip_on_launch=True,
    cidr_block="10.0.3.0/24",
    tags={
        "Name": "subnet-public-c-"+var.PROJECT_NETWORK_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

subnetPrivateA=aws.ec2.Subnet(
    "subnet-private-A",
    vpc_id=infradev.id,
    availability_zone="us-east-1a",
    cidr_block="10.0.11.0/24",
    tags={
        "Name": "subnet-private-a-"+var.PROJECT_NETWORK_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)
    
subnetPrivateB=aws.ec2.Subnet(
    "subnet-private-B",
    vpc_id=infradev.id,
    availability_zone="us-east-1b",
    cidr_block="10.0.12.0/24",
    tags={
        "Name": "subnet-private-b-"+var.PROJECT_NETWORK_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

subnetPrivateC=aws.ec2.Subnet(
    "subnet-private-C",
    vpc_id=infradev.id,
    availability_zone="us-east-1c",
    cidr_block="10.0.13.0/24",
    tags={
        "Name": "subnet-private-c-"+var.PROJECT_NETWORK_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

routeTablePublic=aws.ec2.RouteTable(
    "rtb-public",
    vpc_id=infradev.id,
    routes=[
        aws.ec2.RouteTableRouteArgs(
            cidr_block="0.0.0.0/0",
            gateway_id=igwdev.id
        )
    ],
    tags={
        "Name": "rtb-public-"+var.PROJECT_NETWORK_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

routeTablePrivate=aws.ec2.RouteTable(
    "rtb-private",
    vpc_id=infradev.id,
    routes=[],
    tags={
        "Name": "rtb-private-"+var.PROJECT_NETWORK_NAME+"-"+var.PROJECT_ENVIRONMENT,
        "Cost": var.PROJECT_COST_NAME,
        "Environment": var.PROJECT_ENVIRONMENT
    }
)

routeTablePublicAssocA=aws.ec2.RouteTableAssociation(
    "rtb-public-asoc-A",
    route_table_id=routeTablePublic.id,
    subnet_id=subnetPublicA
)

routeTablePublicAssocB=aws.ec2.RouteTableAssociation(
    "rtb-public-asoc-B",
    route_table_id=routeTablePublic.id,
    subnet_id=subnetPublicB
)

routeTablePublicAssocC=aws.ec2.RouteTableAssociation(
    "rtb-public-asoc-C",
    route_table_id=routeTablePublic.id,
    subnet_id=subnetPublicC
)

routeTablePrivateAssocA=aws.ec2.RouteTableAssociation(
    "rtb-private-asoc-A",
    route_table_id=routeTablePrivate.id,
    subnet_id=subnetPrivateA
)

routeTablePrivateAssocB=aws.ec2.RouteTableAssociation(
    "rtb-private-asoc-B",
    route_table_id=routeTablePrivate.id,
    subnet_id=subnetPrivateB
)

routeTablePrivateAssocC=aws.ec2.RouteTableAssociation(
    "rtb-private-asoc-C",
    route_table_id=routeTablePrivate.id,
    subnet_id=subnetPrivateC
)