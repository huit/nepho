#
# Slap together some basic files depending on the tier.
#


OUTFILE=/var/www/html/index.html
cat <<'EOF' > ${OUTFILE}
<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation_graphic.png" alt="AWS CloudFormation Logo"/>
<h1>Congratulations, you have successfully launched the multi-tier AWS CloudFormation sample.</h1>
<p>This is a multi-tier web application launched in an Amazon Virtual Private Cloud (Amazon VPC) with multiple subnets. 
The first subnet is public and contains and internet facing load balancer, a NAT device for internet 
access from the private subnet and a bastion host to allow SSH access to the hosts in the private subnet. 
The second subnet is private and contains a Frontend fleet of EC2 instances, an internal load balancer 
and a Backend fleet of EC2 instances.</p>
<p>To serve a web page from the backend service, click <a href="/backend/">here</a>.</p>
EOF
chmod 644  ${OUTFILE}
chown root:root ${OUTFILE}

OUTFILE=/etc/httpd/conf.d/maptobackend.conf
cat <<'EOF' > ${OUTFILE}
ProxyPass /backend http://${NEPHO_BACKEND_HOSTNAME}
ProxyPassReverse /backend http://${NEPHO_BACKEND_HOSTNAME}
EOF
chmod 644  ${OUTFILE}
chown root:root ${OUTFILE}

OUTFILE=/var/www/html/backend.html
cat <<'EOF' > ${OUTFILE}
<img src="https://s3.amazonaws.com/cloudformation-examples/cloudformation_graphic.png" alt="AWS CloudFormation Logo"/>
<h1>Congratulations, this request was served from the backend fleet</h1>
EOF
chmod 644  ${OUTFILE}
chown root:root ${OUTFILE}
            
/sbin/chkconfig httpd on
/sbin/service httpd start 
            