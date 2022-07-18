Name:		bkwww
Version:	0.0.1
Release:	1
License:	GPLv3
Summary:	Backup web site
URL:		https://github.com/tieugene/utools/%{name}
Source0:	%{name}-%{version}.tar.bz2
BuildRequires:	systemd-rpm-macros
Requires:	rsync, logrotate, nginx, mariadb
BuildArch:	noarch

%description
%{summary}

%prep
%autosetup

%install
install -p -D -m 0755 %{name}.sh %{buildroot}/usr/local/bin/bkwww.sh
install -p -D -m 0644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -p -D -m 0644 bkwww_x.lst %{buildroot}%{_sysconfdir}/bkwww_x.lst
install -p -D -m 0755 %{name}.cron.daily %{buildroot}%{_sysconfdir}/cron.daily/z_bkwww
install -p -D -m 0644 %{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

%files
%doc README.md
#TODO
#{_bindir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}.conf

%changelog
* Mon Jul 18 2022 TI_Eugene <ti.eugene@gmail.com> - 0.0.1-1
- Initial build
