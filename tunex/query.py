#!/usr/bin/env python

import tunex


class Command:
    @staticmethod
    def create_launch_configuration(autoscaling, storage, security_group):
        return autoscaling.create_launch_configuration(
            LaunchConfigurationName='tunex-cluster',
            ImageId='ami-027583e616ca104df',
            KeyName=storage.get_awspubkeyname(),
            SecurityGroups=[
                str(security_group),
            ],
            UserData='',
            InstanceType='t2.micro',
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sda1',
                    'Ebs': {
                        'SnapshotId': 'snap-0a9bff332c1cc9f5a',
                        'VolumeSize': 8,
                        'VolumeType': 'gp2',
                        'DeleteOnTermination': True,
                    },
                },
            ],
            InstanceMonitoring={
                'Enabled': False
            },
            EbsOptimized=False,
            AssociatePublicIpAddress=True)

    @staticmethod
    def create_sggroup(ec2):
        return ec2.create_security_group(
            Description='ScaleX-tunex cluster security group',
            GroupName='tunex')

    @staticmethod
    def get_sggroup(ec2):
        return ec2.describe_security_groups(
            GroupNames=['tunex'])

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
