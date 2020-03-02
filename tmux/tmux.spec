Name:           tmux
# rc yes, but has a bunch of AIX patches and in my testing, seems fairly reliable
# unfortunately, RPM complains if we put the -rc here
Version:        3.1
Release:        1qsecofr
Summary:        A terminal multiplexer

Group:          Applications/System
# Most of the source is ISC licensed; some of the files in compat/ are 2 and
# 3 clause BSD licensed.
License:        ISC and BSD
URL:            https://tmux.github.io/
# XXX: Remove for non-rc
#Source0:        https://github.com/tmux/tmux/releases/download/%{version}/%{name}-%{version}.tar.gz
Source0:        https://github.com/tmux/tmux/releases/download/%{version}/%{name}-%{version}-rc.tar.gz
Patch0:         tmux-pase.diff

BuildRequires:  libevent-devel, ncurses-devel, libutil-devel
BuildRequires:  autoconf, automake

%description
tmux is a "terminal multiplexer."  It enables a number of terminals (or
windows) to be accessed and controlled from a single terminal.  tmux is
intended to be a simple, modern, BSD-licensed alternative to programs such
as GNU Screen.


%prep

# XXX: Remove for non-rc
#%setup -q
%setup -q -n %{name}-%{version}-rc
%patch0 -p1

%build

export LDFLAGS="-Wl,-blibpath:%{_libdir}:/QOpenSys/usr/lib"
# tmux won't find this itself
export CPPFLAGS="-I%{_includedir}/ncurses"

autoreconf -fiv .
%configure
%make_build

%install
%make_install

%files
%defattr(-, qsys, *none)
%doc CHANGES README
%license COPYING
%{_bindir}/%{name}
%{_mandir}/man1/%{name}.1

%changelog
* Sun Mar 1 2020 Calvin Buckley <calvin@cmpct.info> - 3.1-1secofr
- Bump (to rc, but will for final release; 3.0a problematic on AIX)
- PASE

* Fri Oct 13 2017 Michael Perzl <michael@perzl.org> - 2.5-1
- updated to version 2.5

* Fri Oct 13 2017 Michael Perzl <michael@perzl.org> - 2.3-1
- updated to version 2.3

* Wed Jan 18 2017 Michael Perzl <michael@perzl.org> - 2.2-1
- updated to version 2.2

* Thu Mar 27 2014 Michael Perzl <michael@perzl.org> - 1.9a-1
- updated to version 1.9a

* Thu Apr 04 2013 Michael Perzl <michael@perzl.org> - 1.8-1
- updated to version 1.8

* Mon Oct 15 2012 Michael Perzl <michael@perzl.org> - 1.7-1
- updated to version 1.7

* Fri Jan 27 2012 Michael Perzl <michael@perzl.org> - 1.6-1
- updated to version 1.6

* Thu Sep 22 2011 Michael Perzl <michael@perzl.org> - 1.5-1
- updated to version 1.5

* Thu Sep 22 2011 Michael Perzl <michael@perzl.org> - 1.4-1
- first version for AIX V5.2 and higher
