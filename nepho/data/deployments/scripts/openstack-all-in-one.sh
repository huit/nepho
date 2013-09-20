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

function get_json_entry
{
	local key=$1
	local json=$2
	local python_code="import json,sys;d=json.loads(sys.stdin.read()); print d[\'${key}\']"
	
	echo ${json} | python -c "${python_code}"
}

# get the public & private info about this EC2 instance
yum -y install puppet facter
PUBLIC_HOSTNAME=$( facter ec2_public_hostname )
PUBLIC_IP=$( facter ec2_public_ipv4 )
PRIVATE_HOSTNAME=$( facter hostname )
PRIVATE_IP=$( facter ipaddress )

cd /root

# get Grizzly installed by impersonating CentOS 6.x and enabling EPEL
RELEASE=$( echo $NEPHO_CONFIGS | python -c "import json,sys;d=json.loads(sys.stdin.read()); print d['OpenstackRelease']" )

[ -r /etc/redhat-release ] || echo "CentOS release 6.4 (Final)" > /etc/redhat-release
yum-config-manager --enable epel

perl -i -p -e 's/^PermitRootLogin .*/PermitRootLogin yes/g' /etc/ssh/sshd_config
service sshd restart
cd /root/.ssh && rm -f id_rsa* && ssh-keygen -f id_rsa -t rsa -N '' && cat id_rsa.pub >> authorized_keys

RELEASE_RPM=http://rdo.fedorapeople.org/openstack-${RELEASE}/rdo-release-${RELEASE}.rpm
yum install -y $RELEASE_RPM
yum install -y openstack-packstack openstack-utils
yum -y install policycoreutils sheepdog

cd /root
export HOME=/root

mkdir /media/ephemeral0/mongodb && ln -s /media/ephemeral0/mongodb /var/lib/mongodb
mkdir /media/ephemeral0/glance  && ln -s /media/ephemeral0/glance  /var/lib/mongodb
mkdir /media/ephemeral0/swift   && ln -s /media/ephemeral0/swift   /var/lib/swift  
mkdir /media/ephemeral0/cinder  && ln -s /media/ephemeral0/cinder  /var/lib/cinder

# ********* PACKSTACK *************

# Do packstack
ANS_FILE=/root/packstack-answers.txt

# generate an answers file if not present
[ -f ${ANS_FILE} ] || packstack --gen-answer-file=${ANS_FILE}

# Use openstack-config tool to modify these files
CONFIG="openstack-config --set ${ANS_FILE} "

KEYS=" CONFIG_KEYSTONE_HOST \
       CONFIG_GLANCE_HOST \
       CONFIG_NOVA_API_HOST \
       CONFIG_NOVA_CERT_HOST \
       CONFIG_NOVA_VNCPROXY_HOST \
       CONFIG_NEUTRON_SERVER_HOST \
       CONFIG_SWIFT_PROXY_HOSTS \
       CONFIG_CINDER_HOST \
       CONFIG_HORIZON_HOST \
       CONFIG_HEAT_HOST \
       CONFIG_HEAT_CFN_HOST \
       CONFIG_HEAT_CLOUDWATCH_HOST \
       CONFIG_CEILOMETER_HOST \
       CONFIG_NAGIOS_HOST"

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

# Install HEAT
${CONFIG} general CONFIG_HEAT_INSTALL y
${CONFIG} general CONFIG_HEAT_CLOUDWATCH_INSTALL y
${CONFIG} general CONFIG_HEAT_CFN_INSTALL y

# Do tempest
${CONFIG} general CONFIG_PROVISION_TEMPEST y

# Do tempest
${CONFIG} general CONFIG_CINDER_VOLUMES_SIZE 60G

KEYS=$( echo $NEPHO_CONFIGS | python -c "import json,sys;d=json.loads(sys.stdin.read());for e in d['OpenstackDisabledServices']: print e" )

for KEY in $KEYS; do 
 ${CONFIG} general ${KEY} n
done
# Run packstack 
nohup packstack --answer-file=${ANS_FILE} 

# Seems that the Havana version of packstack needs a little tweaking as to deps, 
#  and we could use some more debugging. Bo for it let's restart 
# all the services after enabling debugging...

DEBUG_CONF_FILES=" /etc/glance/glance-api.conf \
                   /etc/glance/glance-cache.conf \
                   /etc/glance/glance-registry.conf \
                   /etc/glance/glance-scrubber.conf "       

if [ ${RELEASE} = "havana" ]; then

  for f in ${CONF_FILES}; do
      openstack-config --set ${f} general debug True
  done

  # fix the swift proxy-server's bind IP address
  openstack-config --set /etc/swift/proxy-server.conf DEFAULT bind_ip ${PRIVATE_IP}

  perl -i -p -e 's/DEBUG = False/DEBUG = True/' /etc/openstack-dashboard/local_settings

  chkconfig --list | grep openstack | awk '{print $1}' | xargs -ixxx service xxx restart
  chkconfig --list | grep neutron | awk '{print $1}' | xargs -ixxx service xxx restart

  service httpd restart
fi

#
# Setup some extra objects for a usable testing env
#
[ -x /usr/bin/neutron ] && ln -s /usr/bin/neutron /usr/bin/quantum
cd /tmp
git clone https://github.com/robparrott/openstack-post-config.git 
cd ./openstack-post-config
bash ./main.sh

