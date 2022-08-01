%global module ulib
Name:           python-ulib
Version:        0.0.1
Release:        1%{?dist}
License:        GPLv3
Summary:        Utility micro-library
URL:            https://github.com/tieugene/utools/%{module}
Source0:        %{module}-%{version}.tar.xz
BuildRequires:  python3-setuptools
BuildRequires:  systemd-rpm-macros
Requires:       python3 >= 3.6
Suggests:       %{py3_dist libvirt-python}
Suggests:       %{py3_dist appdirs}
BuildArch:      noarch

%description
Common library for micro-tools.


%prep
%autosetup -n %{module}-%{version}


%build
%{py3_build}


%install
%{py3_install}


%files
#license LICENSE
%doc README.md
%{python3_sitelib}/%{module}/
%{python3_sitelib}/%{module}-%{version}-py3.*.egg-info/


%changelog
* Mon Aug 01 2022 TI_Eugene <tieugene@fedoraproject.org> - 0.0.1-1
- Initial build
