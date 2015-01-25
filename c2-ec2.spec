%if 0%{?rhel} && 0%{?rhel} <= 6
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%endif

Name:    c2-ec2
Version: 0.0.1
Release: 1%{?dist}
Summary: CROC Cloud platform API client

Group:   Development/Tools
License: GPLv3
URL:     http://cloud.croc.ru
Source:  %name-%version.tar.gz

BuildArch:     noarch
BuildRequires: python2-devel
BuildRequires: python-setuptools

Requires: python-setuptools python-boto
%if 0%{?rhel} == 6
Requires: python-argparse
%endif

%description
Simple command-line utility for sending custom requests to CROC Cloud platform.


%prep
%setup -n %name-%version -q


%build
%__python2 setup.py build


%install
[ "%buildroot" = "/" ] || rm -rf "%buildroot"

%__python2 setup.py install -O1 \
	--skip-build \
	--root "%buildroot" \
	--install-lib="%python2_sitelib"


%files
%defattr(-,root,root,-)
%python2_sitelib/c2_ec2.py*
%python2_sitelib/c2_ec2-*.egg-info

%_bindir/%name
%doc README.md


%clean
[ "%buildroot" = "/" ] || rm -rf "%buildroot"


%changelog
* Sun Jan 25 2015 Mikhail Ushanov <gm.mephisto@gmail.com> - 0.0.1-1
- New package.
