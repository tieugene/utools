Name:		homesnap
Version:	0.0.1
Release:	1
License:	GPLv3
Summary:	Home backup snapshot
URL:		https://github.com/tieugene/utools/%{name}
Source0:	%{name}-%{version}.tar.xz
BuildRequires:	systemd-rpm-macros
Requires:	systemd
Requires:	rsync
BuildArch:	noarch

%description
%{summary}


%prep
%autosetup


%install
%{__install} -Dpm 0755 %{name}.py %{buildroot}%{_bindir}/%{name}.py
%{__install} -Dpm 0644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
%{__install} -Dpm 0644 %{name}.timer %{buildroot}%{_unitdir}/%{name}.timer


%post
%systemd_post %{name}.{service,timer}


%preun
%systemd_preun %{name}.{service,timer}


%postun
%systemd_postun_with_restart %{name}.{service,timer}


%files
%doc README.md
%{_bindir}/%{name}.py
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer


%changelog
* Mon Aug 01 2022 TI_Eugene <ti.eugene@gmail.com> - 0.0.1-1
- Initial build
