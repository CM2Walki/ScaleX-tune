#!/usr/bin/env python

import boto3


class Context:
    def __init__(self, awssecret, awstoken, awsregion):
        self.session = boto3.session.Session()
        # Hack for mounting boto3 into a binary
        # correlating to https://github.com/boto/boto3/issues/275
        self.session._loader.search_paths.append('/usr/local/lib/python2.7/dist-packages/botocore/data')
        # TODO: Figure out why SSL is breaking
        self.autoscaling = self.session.client('autoscaling',
                                  aws_access_key_id=awstoken,
                                  aws_secret_access_key=awssecret,
                                  region_name=awsregion,
                                  use_ssl=False)
        self.clusterlist = []

    # Retrieve active clusters created by tunex in the past
    def build_context(self):
        # Get all auto scaling groups
        reponse = self.autoscaling.describe_auto_scaling_groups()
        if int(reponse['ResponseMetadata']['HTTPStatusCode']) == 200:
            grouplist = list(reponse['AutoScalingGroups'])
            out = []
            for s in grouplist:
                if str.startswith(str(s), 'tunex-'):
                    out.append(s)
            return out
        else:
            return []
