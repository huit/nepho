OUTDIR=/home/ec2-user

env | sort > ${OUTDIR}/env.txt
cp /var/lib/cloud/data/scripts/part-000 ${OUTDIR}/cloud-init-script.txt
cp /var/log/cloud-init.log ${OUTDIR}/cloud-init-log.txt
cp /var/log/cfn-init.log ${OUTDIR}/cfn-init-log.txt

chown ec2-user:ec2-user ${OUTDIR}/*

# Get latest aws command line client
yum -y install python-pip
python-pip install --upgrade awscli

# get latest s3cmd client
git clone https://github.com/s3tools/s3cmd.git s3cmd
cd s3cmd/
git checkout v1.5.0-alpha3
python setup.py install

cat /etc/aws/credentials | sed 's/aws_access_key_id/access_key/g' | sed 's/aws_secret_access_key/secret_key/g' > ~/.s3cfg  

