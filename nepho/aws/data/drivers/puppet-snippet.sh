#
# Deploy Puppet on a newly provisioned system
#
function deploy_puppet {
    ## Enable Puppet Labs repo

    # Fake a redhat-release
    [ -r /etc/redhat-release ] || echo "CentOS release 6.4 (Final)" > /etc/redhat-release

    # Get the Puppet Labs repo installed
    PUPPETLABS_RPM=http://yum.puppetlabs.com/el/6/products/i386/puppetlabs-release-6-7.noarch.rpm 
    if ! [ -f /etc/yum.repos.d/puppetlabs.repo ]; then
      rpm -ivh ${PUPPETLABS_RPM} || /bin/true
    fi

    # Get EPEL installed
    EPEL_RPM=http://mirror.utexas.edu/epel/6/i386/epel-release-6-8.noarch.rpm
    if ! [ -f /etc/yum.repos.d/epel.repo ]; then
      rpm -ivh ${EPEL_RPM} || /bin/true
    fi

    ## Install Puppet and dependencies

    REQUIRED_PKGS="puppet augeas curl wget s3cmd aws-cli ruby-devel rubygems gcc"

    export PATH="${PATH}:/usr/local/bin"
    PKGS="${REQUIRED_PKGS} ${extra_pkgs}"
    yum -y --enablerepo=epel --enablerepo=puppetlabs* --disableplugin=priorities install ${PKGS}
    yum -y --enablerepo=epel --enablerepo=puppetlabs* --disableplugin=priorities update

    # Install r10k
    puppet resource package r10k provider=gem ensure=present ||
      echo "Unable to install r10k gem: exit code $?"

    # Deploy r10k modules
    if [ -r 'provisioners/puppet/Puppetfile' ]; then
      pushd provisioners/puppet
      HOME=/root PUPPETFILE_DIR=/etc/puppet/modules r10k puppetfile install
      popd
    else
      echo "No Puppetfile found at '${PWD}/provisioners/puppet/Puppetfile', skipping r10k"
    fi
}
#
# Pull private data from S3
#	Takes a set of urls as an argument,
#   and leaves a set of files/dirs in current directory
#
function pull_private_data {
	local urls=$@

	for url in $urls; do	
		protocol=$( echo $url | awk -F: '{print $1}' )

		if [ 'https' = "${protocol}" ]; then
			wget -q ${url}
		fi	
		
		if [ 'git' = "${protocol}" ]; then
			git clone ${url}
		fi				
	
		if [ 's3' = "${protocol}" ]; then
			local fname=$(  echo $url | awk -F/ '{print $NF}' )
			s3cmd get ${url} ${fname}
		fi	
	done
}

#
# pull repo with git
#
function git_pull {

	local repo=$1
	local branch=$2

	if ! [ x = "x${branch}" ]; then
		branch_arg="--branch $branch"
	fi


	git clone ${branch_arg} $repo
	dir=$( echo ${repo} | awk -F/ '{print $NF}' | sed 's/\.git//' )
	cd ${dir}

	git submodule sync || /bin/true
	git submodule update --init  || /bin/true

	echo
}

## Update ourselves
yum -y update

## Pull cloudlet from repo
cd /tmp
git_pull ${NEPHO_GIT_REPO_URL} ${NEPHO_GIT_REPO_BRANCH}

deploy_puppet

if [ -x 'provisioners/bootstrap.sh' ]; then
    ./provisioners/bootstrap.sh
fi
