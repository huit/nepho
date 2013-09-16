#!/bin/bash -v

## Initialize CloudFormation bits
CF_LOG_FILE=/var/log/cfn-init.log
/opt/aws/bin/cfn-init -v --stack ${CF_STACK_NAME} --resource ${CF_RESOURCE} --access-key ${CF_ACCESS_KEY} --secret-key ${CF_SECRET_KEY}  --region ${CF_REGION} >> ${CF_LOG_FILE} 2>&1 || error_exit $(<${CF_LOG_FILE})
