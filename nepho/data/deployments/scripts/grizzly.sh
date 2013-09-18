OUTDIR=/home/ec2-user

env | sort > ${OUTDIR}/env.txt
cp /var/lib/cloud/data/scripts/part-000 ${OUTDIR}/cloud-init-script.txt
cp /var/log/cloud-init.log ${OUTDIR}/cloud-init-log.txt
cp /var/log/cfn-init.log ${OUTDIR}/cfn-init-log.txt

chown ec2-user:ec2-user ${OUTDIR}/*

#***************************

# get latest s3cmd client
git clone https://github.com/s3tools/s3cmd s3cmd
cd s3cmd/
git checkout v1.5.0-alpha3
python setup.py install

cat /etc/aws/credentials | sed 's/aws_access_key_id/access_key/g' | sed 's/aws_secret_access_key/secret_key/g' > ~/.s3cfg  

#*******************************

# get the public info about this instance
yum -y install puppet facter
PUBLIC_HOSTNAME=$( facter ec2_public_hostname )
PUBLIC_IP=$( facter ec2_public_ipv4 )

cd /root

# get Grizzly installed by impersonating CentOS 6.x and enabling EPEL

RELEASE=grizzly

[ -r /etc/redhat-release ] || echo "CentOS release 6.4 (Final)" > /etc/redhat-release
yum-config-manager --enable epel

perl -i -p -e 's/^PermitRootLogin .*/PermitRootLogin yes/g' /etc/ssh/sshd_config
service sshd restart
cd /root/.ssh && rm -f id_rsa* && ssh-keygen -f id_rsa -t rsa -N '' && cat id_rsa.pub >> authorized_keys

RELEASE_RPM=http://rdo.fedorapeople.org/openstack-${RELEASE}/rdo-release-${RELEASE}.rpm
yum install -y $RELEASE_RPM
yum install -y openstack-packstack openstack-utils
yum -y install policycoreutils

cd /root
export HOME=/root

# ********* PACKSTACK *************

# Do packstack
ANS_FILE=/root/answers.txt

# generate an answers file if not present
[ -f ${ANS_FILE} ] || packstack --gen-answer-file=${ANS_FILE}

# Use openstack-config tool to modify these files
CONFIG="openstack-config --set ${ANS_FILE} "

KEYS=" CONFIG_KEYSTONE_HOST \
       CONFIG_GLANCE_HOST \
       CONFIG_NOVA_API_HOST \
       CONFIG_NOVA_CERT_HOST \
       CONFIG_NOVA_VNCPROXY_HOST \
       CONFIG_SWIFT_PROXY_HOSTS \
       CONFIG_CINDER_HOST \
       CONFIG_HORIZON_HOST"

for KEY in $KEYS; do 

   ${CONFIG} general ${KEY} ${PUBLIC_IP}
   
done

# Fix the interface for a single-node installation (use loopback)
${CONFIG} general CONFIG_NOVA_COMPUTE_PRIVIF lo
${CONFIG} general CONFIG_NOVA_NETWORK_PRIVIF lo

# Use Swift
${CONFIG} general CONFIG_SWIFT_INSTALL y

# Use HTTPS for horizon
${CONFIG} general CONFIG_HORIZON_SSL y

# Run packstack 
nohup packstack --answer-file=${ANS_FILE} 
		
cd /tmp
git clone https://github.com/robparrott/openstack-post-config.git 
cd ./openstack-post-config
bash ./main.sh

