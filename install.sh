#!/bin/bash

redhat="/etc/redhat-release"
debian="/etc/debian_version"
flag=

[ -f $redhat ] && flag=$redhat
[ -f $debian ] && flag=$debian

if [ ! -n $flag ]; then
	echo "Can't determine release version"
	exit 1
elif [ $flag = $debian ]; then
	echo "This is debian/ubuntu/mint/../other_shit distro"
	echo "Installing packages..."
	sudo apt-get install python-boto
elif [ $flag = $redhat ]; then
	echo "This is redhat/fedora/centos/../other_fck_shit distro"
	echo "Installing packages..."
	sudo yum install python-boto
fi

sudo install -m 755 c2-ec2 /usr/local/sbin/
