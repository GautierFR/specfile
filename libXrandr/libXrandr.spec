Summary: X.Org X11 libXrandr runtime library
Name: libXrandr
Version: 1.5.2
Release: 1qsecofr
License: MIT
Group: System Environment/Libraries
URL: http://www.x.org

Source0: ftp://ftp.x.org/pub/individual/lib/%{name}-%{version}.tar.bz2

BuildRequires: pkg-config
BuildRequires: util-macros, xorgproto, automake, autoconf
BuildRequires: libX11-devel, libXext-devel, libXrender-devel, libxslt

%description
X.Org X11 libXrandr runtime library

%package devel
Summary: X.Org X11 libXrandr development package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: libX11-devel, libXext-devel, libXrender-devel
Requires: pkg-config

%description devel
X.Org X11 libXrandr development package

%prep
%setup -q


%build
export CONFIG_SHELL=/QOpenSys/pkgs/bin/bash
export CONFIG_ENV_ARGS=/QOpenSys/pkgs/bin/bash

autoreconf -fiv .
%configure \
  CPPFLAGS=-I%{prefix}/libiconv \
  LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
  --with-aix-soname=svr4 \
  --enable-shared --disable-static

%make_build

%install

%make_install

find %{buildroot}/%{_libdir} -name \*.la | xargs rm

%files
%defattr(-, qsys, *none)
%doc COPYING README.md ChangeLog
%{_libdir}/*.so.*

%files devel
%defattr(-, qsys, *none)
%{_includedir}/X11/extensions/*.h
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_mandir}/man3/*.3*

%changelog
* Mon Mar 2 2020 Calvin Buckley <calvin@cmpct.info> - 1.5.2-1qsecofr
- Init

