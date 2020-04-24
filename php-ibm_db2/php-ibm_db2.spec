# XXX: The hardcoding of PHP version is very ugly, need to figure out how to solve elegantly
%define php_version 7.3
Name:        php-ibm_db2
Version:     2.0.8
Release:     10qsecofr
Summary:     Extension for IBM DB2 Universal Database, IBM Cloudscape, and Apache Derby

License:     Apache-2.0
URL:         https://pecl.php.net/package/ibm_db2
Source0:     https://pecl.php.net/get/ibm_db2-%{version}.tgz
Source1:     php-ibm_db2-99-ibm_db2.ini
# begin ugly patchset (XXX: we should upstream and cut a new release, w/ stuff left in master)
Patch1:      0001-db400-doesn-t-like-autocommit-this-way-change-addres.patch
Patch2:      0002-Use-sane-defaults-test-creds-for-PASE.patch
Patch3:      0003-Tests-shouldn-t-use-a-function-removed-in-PHP-7.patch
Patch4:      0004-This-test-would-always-fail-because-it-prints-what-i.patch
Patch5:      0005-Make-sure-this-is-our-default-library.patch
Patch6:      0006-DescribeParam-returns-a-too-small-for-BIGINT-precisi.patch
Patch7:      0007-README-notes-for-PASE-users.patch
Patch8:      0008-Hebrew-test-prints-twice-also-make-it-care-about-the.patch
Patch9:      0009-Fix-nonsense-test-behaviour.patch
Patch10:     0010-Ignore-sqlca-on-PASE.patch
Patch11:     0011-Use-sqlcli-devel-on-PASE-for-headers.patch

BuildRequires: php-devel >= %{php_version}
BuildRequires: sqlcli-devel
# For fix-rpath
BuildRequires: pase-build-tools
# For tests
BuildRequires: php-cli >= %{php_version}
# Misc stuff that it'll throw up without otherwise
BuildRequires: sed-gnu m4-gnu make-gnu

Requires:    php-common >= %{php_version}

%description
This extension supports IBM DB2 Universal Database, IBM
Cloudscape, and Apache Derby databases.

%prep
%setup -q -n ibm_db2-%{version}

# HACK: say no to CRLFs
for file in $(ls tests/*.phpt tests/connection.inc README.md ibm_db2.c config.m4)
do
	sed -i -e 's/\r//g' "$file"
done
# begin ugly patchset
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
#%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1

%build

# Pretend to be AIX so shared libraries work (autoreconf doesn't work)
%define _host powerpc-ibm-aix6.1.9.0
%define _host_alias powerpc-ibm-aix6.1
%define _host_os aix6.1.9.0

phpize --clean
phpize
%configure --with-IBM_DB2=/QOpenSys/usr
%make_build
# for some reason, libtool gets confused and forgets to copy this
cp ./.libs/ibm_db2.so ./modules/
# fix the rpath on the module since we won't let libtool touch see (see %install)
fix-rpath ./modules/ibm_db2.so "/QOpenSys/pkgs/lib:/QOpenSys/usr/lib"

%install

# make install does NOT respect destdir, we will manually install this ourselves
# XXX: have to run mkdir -p and install without -D; i 7.2 specific?
mkdir -p %{buildroot}%{_libdir}/php-%{php_version}/extensions/
install -m 755 modules/ibm_db2.so %{buildroot}%{_libdir}/php-%{php_version}/extensions/ibm_db2.so
install -D -m 644 %{SOURCE1} %{buildroot}%{_sysconfdir}/php/conf.d/99-ibm_db2.ini

# test suite is incredibly fragile
#%check
# gmake test

%files
%defattr(-, qsys, *none)
%doc README LICENSE
%config(noreplace) %{_sysconfdir}/php/conf.d/99-ibm_db2.ini
%{_libdir}/php-%{php_version}/extensions/ibm_db2.so

%changelog
* Tue Dec 3 2019 Calvin Buckley <calvin@cmpct.info> - 2.0.9-9qsecofr
- Fix clobbered INI

* Tue Dec 3 2019 Calvin Buckley <calvin@cmpct.info> - 2.0.9-7qsecofr
- Use CPY instead of Rfile, as Massimo points out

* Mon Dec 2 2019 Calvin Buckley <calvin@cmpct.info - 2.0.8-6qsecofr
- Fix on environments without SQL/CLI headers installed globally
- Polish dependencies further

* Mon Nov 25 2019 Calvin Buckley <calvin@cmpct.info - 2.0.8-5qsecofr
- New specfile for open source PHP RPM

