%global module ulib
Name:           python-ulib
Version:        0.0.2
Release:        1%{?dist}
License:        GPLv3
Summary:        Utility micro-library
URL:            https://github.com/tieugene/utools/%{module}
Source0:        %{module}-%{version}.tar.gz
BuildRequires:  python3 >= 3.9
BuildRequires:  python3-setuptools
BuildRequires:  python3-rpm-macros
Requires:       python3 >= 3.6
Suggests:       %{py3_dist platformdirs}
Suggests:       %{py3_dist sh}
Suggests:       %{py3_dist zstandard}
Suggests:       %{py3_dist sysrsync}
Suggests:       python3-libmount
Suggests:       %{py3_dist libvirt-python}
BuildArch:      noarch

%description
Common library for micro-tools.


%package -n     python3-%{module}
Summary:        %{summary}
%py_provides python3-%{module}

%description -n python3-%{module}
Common library for micro-tools.


%package -n     ulib-backup
Summary:        Backup service
Requires:       %{py3_dist sysrsync}

%description -n ulib-backup
Simple python-based backup.


%prep
%autosetup -n %{module}-%{version}


%build
%{py3_build}


%install
%{py3_install}
%{__install} -Dpm 0644 contrib/backup.service %{buildroot}%{_unitdir}/backup.service
%{__install} -Dpm 0644 contrib/backup.timer %{buildroot}%{_unitdir}/backup.timer


%post -n ulib-backup
%systemd_post backup.{service,timer}


%preun -n ulib-backup
%systemd_preun backup.{service,timer}


%postun -n ulib-backup
%systemd_postun_with_restart backup.{service,timer}


%files -n python3-%{module}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{module}/
%{python3_sitelib}/%{module}-%{version}-py3.*.egg-info/


%files -n ulib-backup
%license LICENSE
%doc doc/README.backup.md backup_sample.py
%{_unitdir}/backup.{service,timer}


%changelog
* Thu Aug 15 2024 TI_Eugene <tieugene@fedoraproject.org> - 0.0.2-1
- backup application added

* Tue Aug 02 2022 TI_Eugene <tieugene@fedoraproject.org> - 0.0.1-1
- Initial build
