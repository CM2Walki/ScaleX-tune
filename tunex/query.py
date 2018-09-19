#!/usr/bin/env python


class Command:
    @staticmethod
    def create_launch_configuration(autoscaling, storage, security_group):
        return autoscaling.create_launch_configuration(
            LaunchConfigurationName='scalectl-cluster',
            ImageId='ami-046f153631cafafdb',
            KeyName=storage.get_awspubkeyname(),
            SecurityGroups=[
                str(security_group),
            ],
            UserData="""#!/bin/bash
            docker run -d -e TARGET="awsloadbal-195663314.eu-central-1.elb.amazonaws.com" -e FUNCTION="(-1)*(x-10)^2+100" --name=benchmark walki/benchmarkcontainer""",
            InstanceType='t2.micro',
            InstanceMonitoring={
                'Enabled': False
            },
            EbsOptimized=False,
            AssociatePublicIpAddress=True)

    @staticmethod
    def create_sggroup(ec2):
        return ec2.create_security_group(
            Description='scalectl cluster security group',
            GroupName='scalectl')

    @staticmethod
    def get_sggroup(ec2):
        return ec2.describe_security_groups(
            GroupNames=['scalectl'])

    # TODO: Make Security Group port rules dependent on the k8s deployments of each cluster
    @staticmethod
    def set_sggroup_access(ec2, security_group):
        return ec2.authorize_security_group_ingress(
            GroupId=str(security_group),
            IpPermissions=[
                {'IpProtocol': 'tcp',
                 'FromPort': 443,
                 'ToPort': 443,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 80,
                 'ToPort': 80,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]},
                {'IpProtocol': 'tcp',
                 'FromPort': 22,
                 'ToPort': 22,
                 'IpRanges': [{'CidrIp': '0.0.0.0/0'}]}
            ])
