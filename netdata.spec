Name: netdata
Version: 1.4.0
Release: 1
Summary: Real-time performance monitoring, done right!
License: GPLv3+
Group: File tools
Url: http://netdata.firehol.org/
# Source-git: https://github.com/firehol/netdata.git
Source0: https://github.com/firehol/netdata/releases/download/v1.4.0/%{name}-%{version}.tar.xz

BuildRequires: zlib-devel
BuildRequires: pkgconfig(uuid)
BuildRequires: pkgconfig(libmnl)
BuildRequires: pkgconfig(libnetfilter_acct)

%description
netdata is the fastest way to visualize metrics. It is a resource
efficient, highly optimized system for collecting and visualizing any
type of realtime timeseries data, from CPU usage, disk activity, SQL
queries, API calls, web site visitors, etc.

netdata tries to visualize the truth of now, in its greatest detail,
so that you can get insights of what is happening now and what just
happened, on your systems and applications.

%prep
%setup -q

%build
autoreconf -fiv
%configure \
	--docdir=%_docdir/%name-%version \
	--with-zlib \
	--with-math \
	--enable-plugin-nfacct \
	--with-user=netdata
%make

%install
%makeinstall_std
rm -rf %buildroot%_libexecdir/netdata/python.d/python_modules/pyyaml{2,3}

mkdir -p %buildroot%_sysconfdir/%name/
install -m 644 -p system/netdata.conf %buildroot%_sysconfdir/%name/netdata.conf

find %buildroot -name .keep | xargs rm

install -d %buildroot%_unitdir/
install -m 644 -p system/netdata.service %buildroot%_unitdir/netdata.service

%pre
%_pre_useradd %{name} /run/%{name} /sbin/nologin
%_pre_groupadd %{name} %{name}

%files
%attr(-,netdata,netdata) %dir %_localstatedir/cache/%name
%attr(-,netdata,netdata) %dir %_localstatedir/log/%name
%dir %_sysconfdir/%name/
%config(noreplace) %_sysconfdir/%name/*.conf
%_sysconfdir/%name/health.d/
%_sysconfdir/%name/python.d/
%_sbindir/%name
%_unitdir/netdata.service
%dir %_libexecdir/%name/
%_libexecdir/%name/charts.d/
%_libexecdir/%name/node.d/
%_libexecdir/%name/plugins.d/
%_libexecdir/%name/python.d/
%dir %_datadir/%name
%_datadir/%name/web
