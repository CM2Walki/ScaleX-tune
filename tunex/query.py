#!/usr/bin/env python

import tunex


class Command:
    @staticmethod
    def create_launch_configuration(client, storage):
        return client.create_launch_configuration(
            LaunchConfigurationName='tunex-cluster',
            ImageId='ami-027583e616ca104df',
            KeyName=storage.get_awspubkeyname(),
            SecurityGroups=[
                'tunex',
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
    def create_sggroup(client):
        return client.create_security_group(
            Description='ScaleX-tunex cluster security group',
            GroupName='tunex')