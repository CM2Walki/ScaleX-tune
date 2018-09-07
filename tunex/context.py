#!/usr/bin/env python

import boto3


class Context:
    def __init__(self, awssecret, awstoken, awsregion):
        self.session = boto3.session.Session()
        # Hack for mounting boto3 into a binary
        # correlating to https://github.com/boto/boto3/issues/275
        self.session._loader.search_paths.append('/usr/local/lib/python2.7/dist-packages/botocore/data')
        self.ec2 = self.session.client('ec2',
                                  aws_access_key_id=awstoken,
                                  aws_secret_access_key=awssecret,
                                  region_name=awsregion)
        self.clusterlist = []
        self.build_context()

    # Retrieve active clusters created by tunex in the past
    def build_context(self):
        response = self.ec2.describe_instances()
        print(response)
