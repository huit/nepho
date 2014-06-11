# coding: utf-8
#
# Parts shamelessly stolen from:
#
#   http://www.technobabelfish.com/2013/08/boto-and-cloudformation.html
#
#
import os
import sys
import time
import yaml
import json
import collections
import shutil
import tempfile
import datetime
from termcolor import colored



from ast import literal_eval

from textwrap import TextWrapper

import signal
from cement.core import exc

import nepho


class OpenStackProvider(nepho.core.provider.AbstractProvider):
    """
    An infrastructure provider class for OpenStack HOT

    Note: if you create an output named SSHEndpoint, then you can
      use the "nepho stack access" command to connect directly to the stack.

    """

    PROVIDER_ID = "OpenStack"
    TEMPLATE_FILENAME = "hot.yaml"

    def __init__(self, config, scenario=None):
        nepho.core.provider.AbstractProvider.__init__(self, config, scenario)
        self.params = {
            'OpenStackAccessKeyID': None,
            'OpenStackSecretAccessKey': None,
            'OpenStackURL': None,
            'KeyName': None,
        }
        self._connection = None
        self._s3_conn = None
        self._iam_conn = None

        if scenario is not None:
            if scenario.name is not None:
                self.stack_name = scenario.name
            else:
                context = scenario.context
                self.stack_name = "%s-%s" % (context['cloudlet']['name'],
                                             context['blueprint']['name'])
        else:
            print "scenario is none"

    @property
    def connection(self):
        """
        Lazy-load connection when needed. This allows for including the provider
        in context creation even though the provider connection requires a valid
        context.
        """
        if self._connection is None:
            (access_key, secret_key, region) = self._load_OpenStack_connection_settings()
            self._connection = boto.cloudformation.connect_to_region(
                region, OpenStack_access_key_id = access_key, OpenStack_secret_access_key = secret_key)
            if self._connection is None:
                print "Boto connection to CloudFormation failed. Please check your credentials."
                exit(1)
        return self._connection

    @property
    def s3_conn(self):
        if self._s3_conn is None:
            (access_key, secret_key, region) = self._load_OpenStack_connection_settings()
            self._s3_conn = boto.s3.connection.S3Connection(
                OpenStack_access_key_id = access_key, OpenStack_secret_access_key = secret_key)
            if self._s3_conn is None:
                print "Boto connection to S3 failed. Please check your credentials."
                exit(1)
        return self._s3_conn

    @property
    def iam_conn(self):
        if self._iam_conn is None:
            (access_key, secret_key, region) = self._load_OpenStack_connection_settings()
            self._iam_conn = boto.iam.connection.IAMConnection(
                OpenStack_access_key_id = access_key, OpenStack_secret_access_key = secret_key)
            if self._iam_conn is None:
                print "Boto connection to IAM failed. Please check your credentials."
                exit(1)
        return self._iam_conn

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

    def create(self, app_obj):
        """Deploy a given pattern."""
        if app_obj.pargs.debug is True:
            boto.set_stream_logger('OpenStack_provider')

        context = self.scenario.context

        raw_template = self.scenario.template

        template_dict = parse_cf_json(raw_template)
        # Minimize JSON to save space
        template_json = json.dumps(template_dict, separators=(',', ':'))

        params = construct_params(context['parameters'], template_dict['Parameters'].keys())

        print " - Determining owner information"
        try:
            iam_user = self.iam_conn.get_user()
        except:
            print colored("Error: ", "red") + "Unable to get IAM username"
            exit(1)

        # Archive payload directory and send to S3
        payload_url = self._send_payload(context, timeout=3600)
        params.append(('PayloadURL', payload_url))

        try:
            print " - Creating CloudFormation stack"
            stack_id = self.connection.create_stack(
                self.stack_name,
                template_body = template_json,
                parameters = params,
                capabilities = ['CAPABILITY_IAM'],
                tags = {
                    'OwnerId': iam_user.user_id,
                    'OwnerName': iam_user.user_name,
                    'CreatedBy': 'nepho'
                },
                disable_rollback = True
            )

            try:
                self._show_status(self.stack_name)
            except exc.CaughtSignal:
                exit()
        except boto.exception.BotoServerError as e:
            print colored("Error: ", "red") + "Problem communicating with CloudFormation"
            # Use e.message instead of e.body as per: https://github.com/boto/boto/issues/1658
            msg = literal_eval(e.message)
            print "(%s) %s " % (msg["Error"]["Code"], msg["Error"]["Message"])
            exit(1)
        return stack_id

    def update(self, app_obj):
        """Update a given pattern."""
        if app_obj.pargs.debug is True:
            boto.set_stream_logger('OpenStack_provider')

        context = self.scenario.context

        raw_template = self.scenario.template

        template_dict = parse_cf_json(raw_template)
        # Minimize JSON to save space
        template_json = json.dumps(template_dict, separators=(',', ':'))

        params = construct_params(context['parameters'], template_dict['Parameters'].keys())

        print " - Determining owner information"
        try:
            iam_user = self.iam_conn.get_user()
        except:
            print colored("Error: ", "red") + "Unable to get IAM username"
            exit(1)

        # Archive payload directory and send to S3
        payload_url = self._send_payload(context, timeout=3600)
        params.append(('PayloadURL', payload_url))

        try:
            print " - Updating CloudFormation stack"
            stack_id = self.connection.update_stack(
                self.stack_name,
                template_body = template_json,
                parameters = params,
                capabilities = ['CAPABILITY_IAM'],
                tags = {
                    'OwnerId': iam_user.user_id,
                    'OwnerName': iam_user.user_name,
                    'CreatedBy': 'nepho'
                },
                disable_rollback = True
            )

            try:
                self._show_status(self.stack_name)
            except exc.CaughtSignal:
                exit()
        except boto.exception.BotoServerError as e:
            print colored("Error: ", "red") + "Problem communicating with CloudFormation"
            # Use e.message instead of e.body as per: https://github.com/boto/boto/issues/1658
            msg = literal_eval(e.message)
            print "(%s) %s " % (msg["Error"]["Code"], msg["Error"]["Message"])
            exit(1)
        return stack_id

    def status(self, app_obj):
        """Check on the status of a stack within CloudFormation."""

        try:
            self._show_status(self.stack_name)
        except exc.CaughtSignal:
            exit()

    def access(self, app_obj):
        try:
            stack = self.connection.describe_stacks(stack_name_or_id=self.stack_name)
        except boto.exception.BotoServerError as e:
            print colored("Error: ", "red") + e.message
            exit(1)

        outputs = stack[0].outputs
        endpoint = [n.value for n in outputs if n.key == 'SSHEndpoint']
        user = [n.value for n in outputs if n.key == 'SSHUser']
        if endpoint:
            endpoint = endpoint.pop()
            if user:
                user = user.pop()
            else:
                user = 'ec2-user'

            os.system("ssh %s@%s" % (user, endpoint))
        else:
            print colored("Error: ", "red") + "No endpoint configured. The stack has not specified the output SSHEndpoint."
            exit(1)

    def destroy(self, app_obj):
        """Delete a CloudFormation stack."""
        self.connection.delete_stack(stack_name_or_id=self.stack_name)

        try:
            self._show_status(self.stack_name)
        except exc.CaughtSignal:
            exit()

    def _load_OpenStack_connection_settings(self):
        context = self.scenario.context
        required_params = ('OpenStackAccessKeyID', 'OpenStackSecretAccessKey', 'OpenStackRegion', 'KeyName')
        for param in required_params:
            if context['parameters'][param] is None:
                print colored("Error: ", "red"), "In order to use the OpenStack provider you must provide valid credentials."
                print "The following parameters are required:"
                print " ", "\n  ".join(required_params)
                print "Use \"nepho parameter set <key> <value>\" to set a parameter."
                exit(1)
        return (
            context['parameters']['OpenStackAccessKeyID'],
            context['parameters']['OpenStackSecretAccessKey'],
            context['parameters']['OpenStackRegion']
        )

    def _send_payload(self, context, timeout):
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
        (access_key, secret_key, region) = self._load_OpenStack_connection_settings()
        try:
            payload_bucket = self.s3_conn.create_bucket(
                'nepho-payloads-' + access_key.lower(), policy='private')

            payload_name = '%s/%s/payload-%s.zip' % (
                context['cloudlet']['name'],
                context['blueprint']['name'],
                datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
            )
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
            return payload_key.generate_url(timeout)
        except Exception as e:
            print colored("Error: ", "red") + "Unable to upload payload to S3"
            print "(%s) %s " % (e.error_code, e.body)
            exit(1)
        finally:
            shutil.rmtree(tmp_dir)

    def _show_status(self, stack):
        while True:
            try:
                stack_update = self.connection.describe_stacks(stack_name_or_id=stack)
                resources = self.connection.list_stack_resources(stack)
            except boto.exception.BotoServerError as e:
                print colored("Error: ", "red") + e.message
                exit(1)
            os.system('cls' if os.name == 'nt' else 'clear')

            su = stack_update[0]

            # Determine terminal display size
            width, height = nepho.core.common.terminal_size()
            if width < 80:
                type_width = 30
                output_width = 54
            else:
                type_width = width - 50
                output_width = width - 31

            print "Name:    %s" % su.stack_name
            print "Created: %s" % su.creation_time
            print "Status:  %s" % colorize_status(su.stack_status)
            print
            print colored(" %-28s %-*s %-18s " % ("Resource", type_width, "Type", "Status"), 'white', 'on_blue')
            for r in resources:
                print " %-28s %-*s %-27s " % (r.logical_resource_id[0:23],
                                              type_width,
                                              r.resource_type[0:type_width],
                                              colorize_status(r.resource_status)[0:27])
            if su.stack_status == "CREATE_COMPLETE" or su.stack_status == "UPDATE_COMPLETE":
                wrapper = TextWrapper(width=output_width)
                print
                print colored(" %-28s %-*s " % ("Output", output_width, "Value"), 'grey', 'on_yellow')
                for o in su.outputs:
                    v = wrapper.wrap(o.value)
                    print " %-28s %-*s " % (o.key[0:28], output_width, v.pop(0))
                    if len(v) > 0:
                        print "                             ", "\n                              ".join(v)
            print "\nMore information: https://console.OpenStack.amazon.com/cloudformation/home"
            if su.stack_status.endswith("FAILED") or su.stack_status.endswith("COMPLETE"):
                break
            else:
                print "Updating in  ",
                for i in xrange(9, -1, -1):
                    sys.stdout.write('\b')
                    sys.stdout.write(str(i))
                    sys.stdout.flush()
                    time.sleep(1)
                print


def colorize_status(status):
    if status.endswith("COMPLETE"):
        return colored(status, "green")
    elif status.endswith("IN_PROGRESS"):
        return colored(status, "yellow")
    elif status.endswith("FAILED"):
        return colored(status, "red")
    else:
        return status


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


def construct_params(possible_params, allowed_params):
    params = list()
    for item in possible_params.items():
        if item[0] in allowed_params:
            if item[1] is None:
                print colored("Error: ", "red"), "Required parameter %s is not set" % item[0]
                exit(1)
            else:
                params.append(item)
        else:
            print colored("Warning: ", "yellow"), "Nepho parameter %s is not present in the CloudFormation template" % item[0]
    return params
