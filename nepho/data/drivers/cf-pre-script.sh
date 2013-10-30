#!/bin/bash -v

function ensure_cfn_tools 
{
 INSTALL_CFN_TOOLS=false
 [ -x /opt/aws/bin/cfn-signal ] || INSTALL_CFN_TOOLS=true
 if [ $INSTALL_CFN_TOOLS = true ]; then
  rpm -ihv http://mirror.utexas.edu/epel/6/i386/epel-release-6-8.noarch.rpm
  yum install -y ruby pystache python-daemon python-requests
  rpm -ihv https://s3.amazonaws.com/cloudformation-examples/aws-cfn-bootstrap-latest.amzn1.noarch.rpm
  rpm -ihv http://s3.amazonaws.com/ec2-downloads/ec2-ami-tools.noarch.rpm
 fi

 yum update -y aws-cfn-bootstrap

}


# Make sure we've got the latest aws-cli command line tools
#
function ensure_updated_awscli
{

 #
 # Make sure we've got the latest aws-cli command line tools
 #

 yum -y install python-pip || yum -y upgrade python-pip
 python-pip install awscli

}

# Helper function
function error_exit {
/opt/aws/bin/cfn-signal -e 1 -r "$1" "${CF_WAIT_HANDLE}"
  exit 1
}

# Try to include various AWS
#
function attempt_aws_tools_update
{

 AWS_PKGS="aws-cli aws-scripts-ses aws-apitools-ec2 aws-amitools-ec2 aws-apitools-mon aws-apitools-elb aws-apitools-rds"
 for P in ${AWS_PKGS}; do
  yum -y install ${P} || /bin/true
 done

}

ensure_cfn_tools
#ensure_updated_awscli
attempt_aws_tools_update

