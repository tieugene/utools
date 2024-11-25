%global module ulib
Name:           python-ulib
Version:        0.0.2
Release:        3%{?dist}
License:        GPLv3
Summary:        Utility micro-library
URL:            https://github.com/tieugene/utools/%{module}
Source0:        %{module}-%{version}.tar.gz
BuildRequires:  python3 >= 3.9
BuildRequires:  python3-setuptools
BuildRequires:  python3-rpm-macros
BuildRequires:  systemd-rpm-macros
Requires:       python3 >= 3.9
Suggests:       %{py3_dist platformdirs}
Suggests:       %{py3_dist sh}
Suggests:       %{py3_dist zstandard}
Suggests:       %{py3_dist sysrsync}
Suggests:       %{py3_dist libvirt-python}
Suggests:       python3-libmount
BuildArch:      noarch

%description
Common library for micro-tools.


%package -n     python3-%{module}
Summary:        %{summary}
#py_provides python3-%%{module}

%description -n python3-%{module}
Common library for micro-tools.


%package -n     ulib-backup
Summary:        Backup service
%if 0%{?epel}
Requires:       python3-%{module}
%else
Requires:       %{py3_dist ulib}
%endif
Requires:       %{py3_dist sh}
Requires:       %{py3_dist zstandard}
Requires:       %{py3_dist sysrsync}
Requires:       %{py3_dist libvirt-python}
Requires:       python3-libmount

%description -n ulib-backup
Simple python-based backup.


%package -n     ulib-homesnap
Summary:        Homesnap service
Requires:       %{py3_dist ulib}
Requires:       %{py3_dist platformdirs}

%description -n ulib-homesnap
Homesnap daemon.


%prep
%autosetup -n %{module}-%{version}


%build
%{py3_build}


%install
%{py3_install}
%{__install} -Dpm 0644 contrib/backup.service %{buildroot}%{_unitdir}/backup.service
%{__install} -Dpm 0644 contrib/backup.timer %{buildroot}%{_unitdir}/backup.timer
%{__install} -Dpm 0644 contrib/homesnap.service %{buildroot}%{_unitdir}/homesnap.service
%{__install} -Dpm 0644 contrib/homesnap.timer %{buildroot}%{_unitdir}/homesnap.timer


%post -n ulib-backup
%systemd_post backup.{service,timer}


%post -n ulib-homesnap
%systemd_post homesnap.{service,timer}


%preun -n ulib-backup
%systemd_preun backup.{service,timer}


%preun -n ulib-homesnap
%systemd_preun homesnap.{service,timer}


%postun -n ulib-backup
%systemd_postun_with_restart backup.{service,timer}


%postun -n ulib-homesnap
%systemd_postun_with_restart homesnap.{service,timer}


%files -n python3-%{module}
%license LICENSE
%doc README.md
%{python3_sitelib}/%{module}/
%{python3_sitelib}/%{module}-%{version}-py3.*.egg-info/


%files -n ulib-backup
%license LICENSE
%doc doc/README.backup.md backup_sample.py
%{_unitdir}/backup.{service,timer}


%files -n ulib-homesnap
%license LICENSE
%doc doc/README.homesnap.md
%{_bindir}/homesnap
%{python3_sitelib}/homesnap.py
%{python3_sitelib}/__pycache__/homesnap.*
%{_unitdir}/homesnap.{service,timer}


%changelog
* Mon Nov 25 2024 TI_Eugene <tieugene@fedoraproject.org> - 0.0.2-3
- bckp: fixed dump_self

* Fri Nov 22 2024 TI_Eugene <tieugene@fedoraproject.org> - 0.0.2-2
- bckp: added opts for rsync-powered functions

* Thu Aug 15 2024 TI_Eugene <tieugene@fedoraproject.org> - 0.0.2-1
- backup application added

* Tue Aug 02 2022 TI_Eugene <tieugene@fedoraproject.org> - 0.0.1-1
- Initial build
