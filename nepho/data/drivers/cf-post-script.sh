#!/bin/bash -v

# Signal completion

/opt/aws/bin/cfn-signal -e $? -r ${CF_RESOURCE} "${CF_WAIT_HANDLE}"
