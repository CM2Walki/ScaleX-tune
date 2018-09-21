#!/usr/bin/env python

from updaterthread import Updater

import boto3
import query


class Context:
    def __init__(self, userstorage, mongodb):
        self.session = boto3.session.Session()
        # Hack for mounting boto3 into a binary
        # correlating to https://github.com/boto/boto3/issues/275
        self.session._loader.search_paths.append('/usr/local/lib/python2.7/dist-packages/botocore/data')
        # TODO: Figure out why SSL is breaking
        self.auto_scaling = self.session.client('autoscaling',
                                                aws_access_key_id=userstorage.get_awstoken(),
                                                aws_secret_access_key=userstorage.get_awssecret(),
                                                region_name=userstorage.get_awsregion(),
                                                use_ssl=False)
        self.ec2 = self.session.client('ec2',
                                       aws_access_key_id=userstorage.get_awstoken(),
                                       aws_secret_access_key=userstorage.get_awssecret(),
                                       region_name=userstorage.get_awsregion(),
                                       use_ssl=False)

        self.elb = self.session.client('elb',
                                       aws_access_key_id=userstorage.get_awstoken(),
                                       aws_secret_access_key=userstorage.get_awssecret(),
                                       region_name=userstorage.get_awsregion(),
                                       use_ssl=False)
        self.userstorage = userstorage
        self.awssubnet2 = userstorage.get_awssubnetid2()
        self.mongodbORM = mongodb
        self.security_group = None
        self.cluster_list = []
        self.cluster_stats = []
        self.updater = None

    # Retrieve active clusters created by scalectl in the past
    def build_context(self, storage):
        # Get all auto scaling groups
        response = self.auto_scaling.describe_auto_scaling_groups()
        answer = ''
        if int(response['ResponseMetadata']['HTTPStatusCode']) == 200:
            # We received something
            group_list = list(response['AutoScalingGroups'])
            out = []
            # Find scalectl clusters that might be running
            for s in group_list:
                if str.startswith(str(s['AutoScalingGroupName']), 'scalectl-'):
                    out.append(s['AutoScalingGroupName'])
                    self.cluster_list.append(s)
            answer += 'User setup successful! Detected %s running scalectl auto scaling cluster(s)' % len(out)
        else:
            answer = 'Daemon error whilst executing describe_auto_scaling_groups (Code: %s)', \
                     response['ResponseMetadata']['HTTPStatusCode']
            return answer
        response = self.auto_scaling.describe_launch_configurations()
        # Get launch configurations
        if int(response['ResponseMetadata']['HTTPStatusCode']) == 200:
            # We received something
            group_list = list(response['LaunchConfigurations'])
            # Find out if launch config exists
            for s in group_list:
                if str.startswith(str(s['LaunchConfigurationName']), 'scalectl-cluster'):
                    answer += '\nFound scalectl-cluster launch configuration'
                    # We found it, it is already created
                    # Get security group id
                    if not self.security_group:
                        response2 = query.Command.get_sggroup(self.ec2)
                        if not int(response2['ResponseMetadata']['HTTPStatusCode']) == 200:
                            return 'Daemon error whilst contacting executing get_sggroup (Code: %ys)', \
                                   response2['ResponseMetadata']['HTTPStatusCode']
                        self.security_group = response2["SecurityGroups"][0]['GroupId']
                    break
            else:
                # It doesn't exist
                # Create security group
                response_sggroup = query.Command.create_sggroup(self.ec2)
                #if not int(response2['ResponseMetadata']['HTTPStatusCode']) == 200:
                #    return 'Daemon error whilst contacting executing create_sggroup (Code: %s)', \
                #           response2['ResponseMetadata']['HTTPStatusCode']
                # Get security group id
                if not self.security_group:
                    response2 = query.Command.get_sggroup(self.ec2)
                    if not int(response2['ResponseMetadata']['HTTPStatusCode']) == 200:
                        return 'Daemon error whilst contacting executing get_sggroup (Code: %s)', \
                                response2['ResponseMetadata']['HTTPStatusCode']
                    self.security_group = response2["SecurityGroups"][0]['GroupId']
                    # Setup security group port rules
                    if len(response_sggroup) != 0:
                        response2 = query.Command.set_sggroup_access(self.ec2, self.security_group)
                        if not int(response2['ResponseMetadata']['HTTPStatusCode']) == 200:
                            return 'Daemon error whilst contacting executing set_sggroup_access (Code: %s)', \
                                    response2['ResponseMetadata']['HTTPStatusCode']
                # Create launch configuration
                response2 = query.Command.create_launch_configuration(self.auto_scaling, storage, self.security_group)
                if not int(response2['ResponseMetadata']['HTTPStatusCode']) == 200:
                    return 'Daemon error whilst contacting executing create_launch_configuration (Code: %s)', \
                           response2['ResponseMetadata']['HTTPStatusCode']
                answer += '\nCreated scalectl-cluster launch configuration'
        else:
            answer = 'Daemon error whilst contacting executing describe_launch_configurations (Code: %s)', \
                     response['ResponseMetadata']['HTTPStatusCode']
            return answer
        return answer

    def run_cluster(self, timestart, timeend, timestep, target, func, clustersize, instancetype):
        answer = "Deleting old launch config"
        query.Command.delete_launch_configuration(self.auto_scaling)
        answer += '\nCreating new launch config'
        response = query.Command.create_launch_configuration(self.auto_scaling, self.userstorage, self.security_group, timestart, timeend, target, timestep, func, instancetype)
        if not int(response['ResponseMetadata']['HTTPStatusCode']) == 200:
            return 'Daemon error whilst contacting executing run_cluster (Code: %s)', \
                   response['ResponseMetadata']['HTTPStatusCode']
        answer += '\nStarting new auto scaling cluster'
        response = query.Command.create_auto_scaling_group(self.auto_scaling, clustersize, self.userstorage)
        if not int(response['ResponseMetadata']['HTTPStatusCode']) == 200:
            return 'Daemon error whilst contacting executing create_auto_scaling_group (Code: %s)', \
                   response['ResponseMetadata']['HTTPStatusCode']
        answer += '\nSuccessfully started cluster'
        self.updater = Updater(1, target, self.mongodbORM, self.userstorage.get_username())
        return answer

    def delete_cluster(self):
        response = query.Command.delete_auto_scaling_group(self.auto_scaling)
        if self.updater:
            self.updater.delete()
        if not int(response['ResponseMetadata']['HTTPStatusCode']) == 200:
            return 'Daemon error whilst contacting executing delete_cluster (Code: %s)', \
                   response['ResponseMetadata']['HTTPStatusCode']
        return "Deleted auto scale cluster"

    def get_cluster_list(self):
        return self.cluster_list

    def get_cluster_stats(self):
        return self.cluster_stats
