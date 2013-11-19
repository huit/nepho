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

# Boto debugging output
#boto.set_stream_logger('foo')

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

        self.connection = self._setup_boto_connection()

    def _setup_boto_connection(self):
        """Helper method to setup a connection to CloudFormation."""

        (access_key, secret_key, region) = self._load_aws_connection_settings()
        if region is None:
            region = 'us-east-1'

        self.s3_conn = boto.s3.connection.S3Connection(
            aws_access_key_id = access_key, aws_secret_access_key = secret_key)
        if self.s3_conn is None:
            print "Boto connection to S3 failed. Please check your credentials."
            exit(1)

        conn = boto.cloudformation.connect_to_region(
            region, aws_access_key_id = access_key, aws_secret_access_key = secret_key)
        if conn is None:
            print "Boto connection to CloudFormation failed. Please check your credentials."
            exit(1)

        self.access_key = access_key

        return conn

#     def validate_template(self, template_str):
#         """Validate the template as JSON and CloudFormation."""
#
#         try:
#             cf_dict = parse_cf_json(template_str)
#             template = get_cf_json(cf_dict, pretty=True)
#             main_args = [
#                 'cloudformation',
#                 'validate-template',
#                 '--template-body', template
#             ]
#             self.clidriver.main(main_args)
#         except:
#             print "Invalid CloudFormation JSON."
#             exit(1)

    def format_template(self, raw_template):
        """Pretty formats a CF template"""

        cf_dict = parse_cf_json(raw_template)
        return get_cf_json(cf_dict, pretty=True)

    def deploy(self):
        """Deploy a given pattern."""

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

        # Upload payload to a public (but obfuscated) S3 bucket
        print " - Creating S3 bucket for payload"
        try:
            payload_bucket = self.s3_conn.create_bucket(
                'nepho-payloads-' + self.access_key.lower(), policy='private')

            payload_name = '%s-payload.tar.gz' % (stack_name)
            payload_key = boto.s3.key.Key(payload_bucket)
            payload_key.key = payload_name
        except:
            print colored("Error: ", "red") + "Unable to create S3 bucket"
            shutil.rmtree(tmp_dir)
            exit(1)

        print " - Uploading payload archive to S3"
        try:
            payload_key.set_contents_from_file(open(payload, 'r'))
            params.append(('PayloadURL', payload_key.generate_url(3600)))
        except Exception as e:
            print colored("Error: ", "red") + "Unable to uplaod payload to S3"
            print e
            exit(1)
        finally:
            shutil.rmtree(tmp_dir)

        try:
            print "The Nepho elves are now building your stack. This may take a few minutes."
            stack_id = self.connection.create_stack(
                stack_name,
                template_body = template_json,
                parameters = params,
                capabilities = ['CAPABILITY_IAM'],
                disable_rollback = True
            )
            print "Your stack ID is %s." % (stack_id)
            print "You can monitor creation progress here: https://console.aws.amazon.com/cloudformation/home"
        except boto.exception.BotoServerError as be:
            print "Error communicating with the CloudFormation service: %s" % (be)
            print "Possible causes:"
            print " - Template error.  Check template validity and ensure all parameters can be accepted by the template."
            print " - Another stack by this name already exists."
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
        """Helper method to load up the conenction settings from configs, or the AWS file."""

        access_key = self.config.get("aws_access_key_id")
        secret_key = self.config.get("aws_secret_access_key")
        region = self.config.get("aws_region")

        try:
            aws_config_file = os.environ['AWS_CONFIG_FILE']
            import ConfigParser
            cp = ConfigParser.ConfigParser()
            cp.read(aws_config_file)

            if access_key is None:
                access_key = cp.get("default", "aws_access_key_id")
            if secret_key is None:
                secret_key = cp.get("default", "aws_secret_access_key")
            if region is None:
                region = cp.get("default", "region")

        except Exception:
            pass

        return (access_key, secret_key, region)


def print_stack(stack):
    print "---"
    print "Name:            %s" % stack.stack_name
    print"ID:              %s" % stack.stack_id
    print "Status:          %s" % stack.stack_status
    print "Creation Time:   %s" % stack.creation_time
    print"Outputs:         %s" % stack.outputs
    print "Parameters:      %s" % stack.parameters
    print"Tags:            %s" % stack.tags
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
