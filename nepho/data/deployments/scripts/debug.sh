OUTDIR=/var/www/html

env | sort > ${OUTDIR}/env.txt
cp /var/lib/cloud/data/scripts/part-000 ${OUTDIR}/cloud-init-script.txt
cp /var/log/cloud-init.log ${OUTDIR}/cloud-init-log.txt
cp /var/log/cfn-init.log ${OUTDIR}/cfn-init-log.txt

OUTFILE=/var/www/html/index.html
cat <<'EOF' > ${OUTFILE}
<html>
<body>
<h1>AWS CloudFormation Debuging</h1>
<hr/>
<ul>
<li><a href="env.txt">environment</a></li>
<li><a href="cloud-init-script.txt">cloud-init script</a></li>
<li><a href="cloud-init-log.txt">cloud-init log</a></li>
<li><a href="cfn-init-log.txt">cfn-init log</a></li>
</ul>
</body>
</html>
EOF
chmod 644  ${OUTDIR}/*
chown root:root ${OUTFILE}

/sbin/chkconfig httpd on
/sbin/service httpd start 