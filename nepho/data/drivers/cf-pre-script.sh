#!/bin/bash -v

yum update -y aws-cfn-bootstrap

# Helper function
function error_exit {
/opt/aws/bin/cfn-signal -e 1 -r "$1" "${CF_WAIT_HANDLE}"
  exit 1
}
        