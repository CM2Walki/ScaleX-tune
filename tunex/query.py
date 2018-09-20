#!/usr/bin/env python

from botocore.exceptions import ClientError


class Command:
    @staticmethod
    def create_launch_configuration(autoscaling, storage, security_group, timestart=0, timeend=2147483647, target="1.2.3.4", timestep=60, function="(-1)*(x-10)^2+100", instancetype="t2.micro"):
        return autoscaling.create_launch_configuration(
            LaunchConfigurationName='scalectl-cluster',
            ImageId='ami-046f153631cafafdb',
            KeyName=storage.get_awspubkeyname(),
            SecurityGroups=[
                str(security_group),
            ],
            UserData="""#!/bin/bash\ndocker run -d -e TIMESTART=""" + str(timestart) +
                     """-e TIMEEND=""" + str(timeend) +
                     """-e TIMESTEP=""" + str(timestep) +
                     """-e TARGET=""" + str(target) +
                     """-e FUNCTION=""" + str(function) + """ --name=benchmark walki/benchmarkcontainer\nsudo systemctl stop update-engine""",
            InstanceType=instancetype,
            InstanceMonitoring={
                'Enabled': False
            },
            EbsOptimized=False,
            AssociatePublicIpAddress=True)

    @staticmethod
    def delete_launch_configuration(autoscaling):
        try:
            Command.delete_auto_scaling_group(autoscaling)
        except ClientError as e:
            print ""
        try:
            return autoscaling.delete_launch_configuration(
                LaunchConfigurationName='scalectl-cluster')
        except ClientError as e:
            return []

    @staticmethod
    def delete_auto_scaling_group(autoscaling):
        return autoscaling.delete_auto_scaling_group(
            AutoScalingGroupName='scalectl-cluster-benchmark',
            ForceDelete=True)

    @staticmethod
    def create_auto_scaling_group(autoscaling, size, storage):
        return autoscaling.create_auto_scaling_group(
            AutoScalingGroupName='scalectl-cluster-benchmark',
            LaunchConfigurationName='scalectl-cluster',
            MinSize=size,
            MaxSize=size,
            DefaultCooldown=0,
            VPCZoneIdentifier=str(storage.get_awssubnetid2())
        )

    @staticmethod
    def create_sggroup(ec2):
        try:
            response = ec2.create_security_group(
                Description='scalectl cluster security group',
                GroupName='scalectl')
            return response
        except ClientError as e:
            return []

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
