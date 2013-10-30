#!/bin/bash -v\
yum update -y aws-cfn-bootstrap

# Helper function,
function error_exit
{
 /opt/aws/bin/cfn-signal -e 1 -r "$1" '", { "Ref" : "{{ name }}WaitHandle" }, "'
exit 1
}

## Initialize CloudFormation bits
/opt/aws/bin/cfn-init -v  --stack ", { "Ref" : "AWS::StackName" },  --resource {{ name }}Instance",
          "   --access-key ",  { "Ref" : "{{ name }}Keys" },
          "   --secret-key ", {"Fn::GetAtt": ["{{ name }}Keys", "SecretAccessKey"]},
          "   --region ", { "Ref" : "AWS::Region" }, " > /tmp/cfn-init.log 2>&1 || error_exit $(</tmp/cfn-init.log),

# pull & setup puppet modules and run manifest
NEPHO_GIT_REPO_URL='", { "Ref" : "GitRepo" }, "'
NEPHO_GIT_REPO_BRANCH='", { "Ref" : "GitRepoBranch" }, "'