# coding: utf-8
#
# Parts shamelessly stolen from:
#
#   http://www.technobabelfish.com/2013/08/boto-and-cloudformation.html
#
#
import os
import yaml
import json
import collections
import shutil
import tempfile
from termcolor import colored

import boto
import boto.cloudformation
import boto.s3.connection

from ast import literal_eval

import nepho


class AWSProvider(nepho.core.provider.AbstractProvider):
    """
    An infrastructure provider class for AWS CloudFormation

    Note: if you create an output named SSHEndpoint, then you can
      use the "nepho stack access" command to connect directly to the stack.

    """

    PROVIDER_ID = "aws"
    TEMPLATE_FILENAME = "cf.json"

    def __init__(self, config, scenario=None):
        nepho.core.provider.AbstractProvider.__init__(self, config, scenario)
        self.params = {
            'AWSAccessKeyID': None,
            'AWSSecretAccessKey': None,
            'AWSRegion': None,
            'KeyName': None,
        }
        self._connection = None
        self._s3_conn = None

    @property
    def connection(self):
        """
        Lazy-load connection when needed. This allows for including the provider
        in context creation even though the provider connection requires a valid
        context.
        """
        if self._connection is None:
            (access_key, secret_key, region) = self._load_aws_connection_settings()
            self._connection = boto.cloudformation.connect_to_region(
                region, aws_access_key_id = access_key, aws_secret_access_key = secret_key)
            if self._connection is None:
                print "Boto connection to CloudFormation failed. Please check your credentials."
                exit(1)
        return self._connection

    @property
    def s3_conn(self):
        if self._s3_conn is None:
            (access_key, secret_key, region) = self._load_aws_connection_settings()
            self._s3_conn = boto.s3.connection.S3Connection(
                aws_access_key_id = access_key, aws_secret_access_key = secret_key)
            if self._s3_conn is None:
                print "Boto connection to S3 failed. Please check your credentials."
                exit(1)
        return self._s3_conn

    def validate_template(self, template_str):

        # Attempt to validate that template is valid JSON, and clean it up
        try:
            template_dict = json.loads(template_str)
            template_str  = json.dumps(template_dict, indent=2, separators=(',', ': '))
        except Exception as e:
            ret = "Validation:\n  Template JSON is not valid!\n"
            ret += "Error:\n  %s\n" % (e)
            return ret

        try:
            compact_template = json.dumps(json.loads(template_str), separators=(',', ':'))
            t = self.connection.validate_template(template_body=compact_template)

            ret = "Validation:\n  Template is valid\n"
            ret += "Description:\n %s\n" % t.description
            ret += "Parameters:"
            for p in t.template_parameters:
                ret += "\n  %s" % (p.parameter_key)
        except boto.exception.BotoServerError as e:
            ret = "Boto Server Error:\n  Template is not valid!\n"
            ret += "Error:\n  %s\n" % (e.error_code)
            ret += "Description:\n  %s" % (e.body)
        return ret

    def format_template(self, raw_template):
        """Pretty formats a CF template"""

        cf_dict = parse_cf_json(raw_template)
        return get_cf_json(cf_dict, pretty=True)

    def deploy(self, debug=None):
        """Deploy a given pattern."""
        if debug is True:
            boto.set_stream_logger('aws_provider')

        context = self.scenario.context

        stack_name = create_stack_name(context)

        raw_template = self.scenario.template
        template_json = self.format_template(raw_template)

        params = list()
        for item in context['parameters'].items():
            params.append(item)

        print " - Archiving payload for upload to S3"
        try:
            tmp_dir = tempfile.mkdtemp()
            payload = shutil.make_archive(
                os.path.join(tmp_dir, 'payload'), 'zip',
                os.path.join(context['cloudlet']['path'], 'payload'))
        except:
            print colored("Error: ", "red") + "Unable to create payload file"
            shutil.rmtree(tmp_dir)
            exit(1)

        # Upload payload to a private S3 bucket
        print " - Creating S3 bucket for payload"
        (access_key, secret_key, region) = self._load_aws_connection_settings()
        try:
            payload_bucket = self.s3_conn.create_bucket(
                'nepho-payloads-' + access_key.lower(), policy='private')

            payload_name = '%s/%s/payload.zip' % (context['cloudlet']['name'], context['blueprint']['name'])
            payload_key = boto.s3.key.Key(payload_bucket)
            payload_key.key = payload_name
        except Exception as e:
            print colored("Error: ", "red") + "Unable to create S3 bucket"
            print "(%s) %s " % (e.error_code, e.body)
            shutil.rmtree(tmp_dir)
            exit(1)

        print " - Uploading payload archive to S3"
        try:
            payload_key.set_contents_from_file(open(payload, 'rb'))
            params.append(('PayloadURL', payload_key.generate_url(3600)))
        except Exception as e:
            print colored("Error: ", "red") + "Unable to upload payload to S3"
            print "(%s) %s " % (e.error_code, e.body)
            exit(1)
        finally:
            shutil.rmtree(tmp_dir)

        try:
            # Use minimal size representation of this JSON string
            compact_template_json = json.dumps(json.loads(template_json), separators=(',', ':'))

            print "The Nepho elves are now building your stack. This may take a few minutes."
            stack_id = self.connection.create_stack(
                stack_name,
                template_body = compact_template_json,
                parameters = params,
                capabilities = ['CAPABILITY_IAM'],
                disable_rollback = True
            )
            print "Your stack ID is %s." % (stack_id)
            print "You can monitor creation progress here: https://console.aws.amazon.com/cloudformation/home"
        except boto.exception.BotoServerError as e:
            print colored("Error: ", "red") + "Problem communicating with CloudFormation"
            # Use e.message instead of e.body as per: https://github.com/boto/boto/issues/1658
            msg = literal_eval(e.message)
            print "(%s) %s " % (msg["Error"]["Code"], msg["Error"]["Message"])
            exit(1)
        return stack_id

    def status(self):
        """Check on the status of a stack within CloudFormation."""

        context = self.scenario.context
        stack_name = create_stack_name(context)

        # Return object of type boto.cloudformation.stack.Stack
        try:
            stack = self.connection.describe_stacks(stack_name_or_id=stack_name)
        except boto.exception.BotoServerError as be:
            # Actually ,this may just mean that there's no stack by that name ...
            print "Error communication with the CloudFormation service: %s" % (be)
            exit(1)

        # Just for now ...
        print_stack(stack[0])
        return stack[0]

    def access(self):
        """Check on the status of a stack within CloudFormation."""

        context = self.scenario.context
        stack_name = create_stack_name(context)

        # Return object of type boto.cloudformation.stack.Stack
        try:
            stack = self.connection.describe_stacks(stack_name_or_id=stack_name)

            # this will need to be improved ... basically a stub for now ...
            outputs = stack.outputs
            access_hostname = outputs['SSHEndpoint']
            return "ssh %s@%s" % ("ec2-user", access_hostname)
        except boto.exception.BotoServerError as be:
            # Actually ,this may just mean that there's no stack by that name ...
            print "Error communication with the CloudFormation service: %s" % (be)
            exit(1)

        # Just for now ...
        print_stack(stack[0])
        return stack[0]

    def destroy(self):
        """Delete a CloudFormation stack."""

        context = self.scenario.context

        stack_name = create_stack_name(context)

        out = self.connection.delete_stack(stack_name_or_id=stack_name)

        print out
        return out

    #===========================================================================
    # These are example helper functions for capabilities not yet needed.
    #===========================================================================

    def _get_stacks(self):
        """Return a list of CF stacks."""
        return self.connection.list_stack()

    def _get_stack(self, stack):
        context = self.scenario.context
        stack_name = create_stack_name(context)

        stacks = self.connection.describe_stacks(stack_name)
        if not stacks:
            raise Exception(stack)

        return stacks[0]

    def _list_stacks(self):
        stacks = self.get_stacks()
        for stackSumm in stacks:
            print_stack(self._get_stack(stackSumm.stack_id))

    def _load_aws_connection_settings(self):
        context = self.scenario.context
        required_params = ('AWSAccessKeyID', 'AWSSecretAccessKey', 'AWSRegion', 'KeyName')
        for param in required_params:
            if context['parameters'][param] is None:
                print colored("Error: ", "red"), "In order to use the AWS provider you must provide valid credentials."
                print "The following parameters are required:"
                print " ", "\n  ".join(required_params)
                print "Use \"nepho parameter set <key> <value>\" to set a parameter."
                exit(1)
        return (
            context['parameters']['AWSAccessKeyID'],
            context['parameters']['AWSSecretAccessKey'],
            context['parameters']['AWSRegion']
        )


def print_stack(stack):
    print "Name:            %s" % stack.stack_name
    print "ID:              %s" % stack.stack_id
    print "Status:          %s" % stack.stack_status
    print "Creation Time:   %s" % stack.creation_time
    print "Outputs:         %s" % stack.outputs
    print "Parameters:      %s" % stack.parameters
    print "Tags:            %s" % stack.tags
    print "Capabilities:    %s" % stack.capabilities


def create_stack_name(context):
    return "%s-%s" % (context['cloudlet']['name'], context['blueprint']['name'])


def parse_cf_json(str):
    try:
        cf_dict = json.loads(str, object_pairs_hook=collections.OrderedDict)
    except ValueError as e:
        print "Error loading JSON template file."
        print e
        exit(1)
    else:
        return cf_dict


def get_cf_json(order_dict, pretty=False):
    outstr = None
    if pretty:
        outstr = json.dumps(order_dict, indent=2, separators=(',', ': '))
    else:
        outstr = json.dumps(order_dict)
    return outstr
