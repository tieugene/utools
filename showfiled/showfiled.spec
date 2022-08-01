Name:           showfiled
Version:        0.0.1
Release:        1%{?dist}
License:        GPLv3
Summary:        Show a file daemon
URL:            https://github.com/tieugene/utools/%{name}
Source0:        %{name}-%{version}.tar.xz
BuildRequires:  systemd-rpm-macros
Requires:       python3 >= 3.5
Requires:       systemd
BuildArch:      noarch

%description
Show a file content by HTTP request.


%prep
%autosetup


%install
%{__install} -Dp -m0755 %{name}.py %{buildroot}%{_sbindir}/%{name}.py
%{__install} -Dp -m0644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
%{__install} -Dp -m0644 %{name}.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/%{name}


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%files
#license LICENSE
%doc README.md
%{_sbindir}/%{name}.py
%{_unitdir}/%{name}.service
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}


%changelog
* Thu Jun 23 2022 TI_Eugene <tieugene@fedoraproject.org> - 0.0.1-1
- Initial build
