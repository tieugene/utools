# use `rpmbuild -ta bkwww-0.0.1.tar.xz` to build rpm
Name:		bkwww
Version:	0.0.1
Release:	1
License:	GPLv3
Summary:	Backup web site
URL:		https://github.com/tieugene/utools/%{name}
Source0:	%{name}-%{version}.tar.xz
BuildRequires:	systemd-rpm-macros
Requires:	rsync, nginx, mariadb
Recommends:	logrotate
BuildArch:	noarch

%description
%{summary}

%prep
%autosetup

%install
install -Dpm 0755 %{name}.sh %{buildroot}%{_bindir}/%{name}.sh
install -Dpm 0644 %{name}.conf %{buildroot}%{_sysconfdir}/%{name}.conf
install -Dpm 0755 %{name}.cron %{buildroot}%{_sysconfdir}/cron.daily/z_bkwww
install -Dpm 0644 %{name}.logrotate %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
install -dpm 0644 %{buildroot}/var/log/%{name}

%files
%doc README.md bkwww_x.lst my.cnf
#TODO
%{_bindir}/%{name}.sh
%config(noreplace) %{_sysconfdir}/%{name}.conf
%{_sysconfdir}/cron.daily/z_bkwww
%{_sysconfdir}/logrotate.d/%{name}
/var/log/%{name}

%changelog
* Mon Jul 18 2022 TI_Eugene <ti.eugene@gmail.com> - 0.0.1-1
- Initial build
