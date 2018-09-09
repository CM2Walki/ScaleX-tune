#!/usr/bin/env python


class QueryData:
    @staticmethod
    def create_launch_configuration(client, storage):
        client.create_launch_configuration(
            LaunchConfigurationName='tunex-cluster',
            ImageId='ami-027583e616ca104df',
            KeyName=storage.get_awspubkeyname(),
            SecurityGroups=[
                'sg-tunex',
            ],
            ClassicLinkVPCId='',
            ClassicLinkVPCSecurityGroups=[
                '',
            ],
            UserData='string',
            InstanceId='string',
            InstanceType='t2.micro',
            KernelId='',
            RamdiskId='',
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
