export MOUNT_PATH=/srv/s3
export YAS3FS_PATH=/opt/yas3fs
export BUCKET_PATH=
export LOG_PATH=/var/log

yum update python-boto
python-pip install fusepy

git clone git://github.com/danilop/yas3fs.git $YAS3FS_PATH
sed -i'' 's/^# user_allow_other/user_allow_other/' /etc/fuse.conf # uncomment user_allow_other

YAS3FS_CMD=" $YAS3FS_PATH/yas3fs.py $MOUNT_PATH "
YAS3FS_CMD=" $YAS3FS_CMD  --region $AWS_REGION "
YAS3FS_CMD=" $YAS3FS_CMD  --url s3://${NEPHO_S3_BUCKET}/${BUCKET_PATH} "
YAS3FS_CMD=" $YAS3FS_CMD  --mkdir "
YAS3FS_CMD=" $YAS3FS_CMD   --log $LOG_PATH/yas3fs.log "
#YAS3FS_CMD=" $YAS3FS_CMD  --topic ${NEPHO_SNS_TOPIC} --new-queue "

echo $YAS3FS_CMD
$YAS3FS_CMD



