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

cd /root

# get Grizzly installed by impersonating CentOS 6.x and enabling EPEL

[ -r /etc/redhat-release ] || echo "CentOS release 6.4 (Final)" > /etc/redhat-release
yum-config-manager --enable epel

perl -i -p -e 's/^PermitRootLogin .*/PermitRootLogin yes/g' /etc/ssh/sshd_config
service sshd restart
cd /root/.ssh && rm -f id_rsa* && ssh-keygen -f id_rsa -t rsa -N '' && cat id_rsa.pub >> authorized_keys

RELEASE_RPM=http://rdo.fedorapeople.org/openstack-grizzly/rdo-release-grizzly.rpm
yum install -y $RELEASE_RPM
yum install -y openstack-packstack
yum -y install policycoreutils

#URL_ROOT=http://mirror.seas.harvard.edu/centos/6/os/x86_64/Packages
#RPMS="qpid-cpp-client-0.14-22.el6_3.x86_64.rpm qpid-cpp-server-0.14-22.el6_3.x86_64.rpm python-lxml-2.2.3-1.1.el6.x86_64.rpm"
#for R in ${RPMS}; do
	#	rpm -ihv ${URL_RO#OT}/${R}
#done
cd /root
export HOME=/root
nohup packstack --allinone
		
cd /tmp
git clone https://github.com/robparrott/openstack-post-config.git 
cd ./openstack-post-config
bash ./main.sh

		