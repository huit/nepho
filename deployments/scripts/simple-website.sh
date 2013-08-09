OUTFILE=/var/www/html/index.php
cat <<'EOF' > ${OUTFILE}
<?php
echo '<h1>AWS CloudFormation sample PHP application</h1>';
?>
EOF
chmod 644  ${OUTFILE}
chown root:root ${OUTFILE}

/sbin/chkconfig httpd on
/sbin/service httpd start 