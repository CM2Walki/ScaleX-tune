#!/usr/bin/env python

import boto3


class Context:
    def __init__(self, awssecret, awstoken, awsregion):
        self.session = boto3.session.Session()
        # Hack for mounting boto3 into a binary
        # correlating to https://github.com/boto/boto3/issues/275
        self.session._loader.search_paths.append('/usr/local/lib/python2.7/dist-packages/botocore/data')
        # TODO: Figure out why SSL is breaking
        self.auto_scaling = self.session.client('autoscaling',
                                  aws_access_key_id=awstoken,
                                  aws_secret_access_key=awssecret,
                                  region_name=awsregion,
                                  use_ssl=False)
        self.cluster_list = []

    # Retrieve active clusters created by tunex in the past
    def build_context(self):
        # Get all auto scaling groups
        response = self.auto_scaling.describe_auto_scaling_groups()
        answer = ''
        if int(response['ResponseMetadata']['HTTPStatusCode']) == 200:
            # We received something
            group_list = list(response['AutoScalingGroups'])
            out = []
            # Find tunex clusters that might be running
            for s in group_list:
                if str.startswith(str(s['AutoScalingGroupName']), 'tunex-'):
                    out.append(s['AutoScalingGroupName'])
                    self.cluster_list.append(s)
            answer += 'User setup successful! Detected %s running tunex auto scaling cluster(s)' % len(out)
        else:
            answer = 'Daemon error whilst executing describe_auto_scaling_groups (Code: %s)', response['ResponseMetadata']['HTTPStatusCode']
            return answer
        response = self.auto_scaling.describe_launch_configurations()
        # Get launch configurations
        if int(response['ResponseMetadata']['HTTPStatusCode']) == 200:
            # We received something
            group_list = list(response['LaunchConfigurations'])
            out = []
            # Find tunex clusters that might be running
            for s in group_list:
                if str.startswith(str(s['LaunchConfigurationName']), 'tunex-cluster'):
                    answer += '\nFound tunex-cluster launch configuration\n%s', str(group_list)
                    break
            else:
                response2 = self.auto_scaling.create_launch_configuration()
                answer += '\nUnable to find tunex-cluster launch configuration'
        else:
            answer = 'Daemon error whilst contacting executing describe_launch_configurations (Code: %s)', response['ResponseMetadata']['HTTPStatusCode']
        return answer
