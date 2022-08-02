%global module ulib
Name:           python-ulib
Version:        0.0.1
Release:        1%{?dist}
License:        GPLv3
Summary:        Utility micro-library
URL:            https://github.com/tieugene/utools/%{module}
Source0:        %{module}-%{version}.tar.xz
BuildRequires:  python3 >= 3.6
BuildRequires:  python3-setuptools
BuildRequires:  python3-rpm-macros
Requires:       python3 >= 3.6
Suggests:       %{py3_dist libvirt-python}
Suggests:       %{py3_dist appdirs}
BuildArch:      noarch

%description
Common library for micro-tools.

%package -n     python3-%{module}
Summary:        %{summary}
%py_provides python3-%{module}

%description -n python3-%{module}
Common library for micro-tools.

%prep
%autosetup -n %{module}-%{version}


%build
%{py3_build}


%install
%{py3_install}


%files -n python3-%{module}
#license LICENSE
%doc README.md
%{python3_sitelib}/%{module}/
%{python3_sitelib}/%{module}-%{version}-py3.*.egg-info/


%changelog
* Tue Aug 02 2022 TI_Eugene <tieugene@fedoraproject.org> - 0.0.1-1
- Initial build
