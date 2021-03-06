# This was autogenerated, but is altered to use a source tarball.
# (And PASE conventions.)

%define real_name libgdiplus

Name:           libgdiplus0
Version:        6.0.2
Release:        1qsecofr
License:        LGPL v2.1 only ; MPL ; MIT License (or similar)
Url:            http://go-mono.org/
Source0:        http://download.mono-project.com/sources/libgdiplus/%{real_name}-%{version}.tar.gz
Summary:        Open Source Implementation of the GDI+ API
Group:          Development/Libraries/Other
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Obsoletes:      libgdiplus-devel
Provides:       libgdiplus-devel
Obsoletes:      libgdiplus
Provides:       libgdiplus

BuildRequires:  cairo-devel >= 1.6.4
BuildRequires:  fontconfig-devel
BuildRequires:  giflib-devel
BuildRequires:  glib2-devel
BuildRequires:  libexif-devel
BuildRequires:  libX11-devel
# XXX: Elsewhere, this is libjpeg-devel. That pkg should have a "provides"
BuildRequires:  libjpeg-turbo-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
%if 0%{?suse_version}
BuildRequires:  freetype2-devel
%else
BuildRequires:  freetype-devel
%endif
# PASE specific; declare stuff RPM has implied dependencies on, plus the fact
# we're using autotools (to regen for lib stuff) which has some implied deps of
# its own. And gcc, since PASE ships with no compilers.
BuildRequires:  gcc-aix, autoconf, automake, libtool, make-gnu, tar-gnu, gawk
BuildRequires:  diffutils, m4-gnu, patch-gnu, coreutils-gnu, grep-gnu, gzip

%description
This is part of the Mono project. It is required when using
Windows.Forms.

%files
%defattr(-, qsys, *none)
# It's OK to include both .so and .so.x because this is for Mono, and not for
# external consumption.
%_libdir/libgdiplus.so*
%_libdir/pkgconfig/libgdiplus.pc
%doc AUTHORS COPYING ChangeLog* NEWS README*

%prep
%setup -q -n %{real_name}-%{version}

%build
# export CFLAGS="$RPM_OPT_FLAGS"
autoreconf -fiv
# XXX: libdsiplus needs -lm but this isn't specified by the makefile, will need patches
%configure \
    CPPFLAGS="-D_LINUX_SOURCE_COMPAT -pthread" \
    LDFLAGS="-pthread -Wl,-brtl -Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib -L%{_libdir}" \
    --with-aix-soname=svr4 \
    --enable-shared --disable-static

%make_build
gmake check || true

%install
%make_install
rm -f %{buildroot}%{_libdir}/libgdiplus.la
# Remove generic non-usefull INSTALL file... (appeases
#  suse rpmlint checks, saves 3kb)
find . -name INSTALL | xargs rm -f

%changelog
* Wed Jan 1 2020 Calvin Buckley  - 6.0.2-1qsecofr
- Bump
- Use IBM tiff/gif

* Sun Aug 04 2019 Calvin Buckley - 6.0-1
- Bump to latest stable and remove obsoleted patch
- Use linux source compat for a less crumbly libgdiplus (remaining test failures are not longer memory related, but seemingly endian)
