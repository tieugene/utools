Name:		homesnap
Version:	0.0.1
Release:	1%{?dist}
License:	GPLv3
Summary:	Home backup snapshot
URL:		https://github.com/tieugene/utools/%{name}
Source0:	%{name}-%{version}.tar.xz
BuildRequires:  python3 >= 3.6
BuildRequires:  python3-setuptools
BuildRequires:  python3-rpm-macros
BuildRequires:	systemd-rpm-macros
Requires:	systemd
Requires:	/usr/bin/rsync
Requires:	%{py3_dist ulib}
Requires:	%{py3_dist appdirs}
BuildArch:	noarch

%description
%{summary}


%prep
%autosetup


%build
%{py3_build}


%install
%{py3_install}
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
%{_bindir}/%{name}
%{python3_sitelib}/%{name}.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{name}-%{version}-py3.*.egg-info/
%{_unitdir}/%{name}.service
%{_unitdir}/%{name}.timer


%changelog
* Mon Aug 01 2022 TI_Eugene <ti.eugene@gmail.com> - 0.0.1-1
- Initial build
