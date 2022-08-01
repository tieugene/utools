Name:           ulib
Version:        0.0.1
Release:        1%{?dist}
License:        GPLv3
Summary:        Utility micro-library
URL:            https://github.com/tieugene/utools/%{name}
Source0:        %{name}-%{version}.tar.xz
BuildRequires:  systemd-rpm-macros
Requires:       python3 >= 3.6
Suggests:       %{py3_dist libvirt-python}
Suggests:       %{py3_dist appdirs}
BuildArch:      noarch

%description
Common library for micro-tools.


%prep
%autosetup


%install
%{__install} -Dpm 0755 %{name}.py %{buildroot}%{_sbindir}/%{name}.py
%{__install} -Dpm 0644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service


%files
#license LICENSE
%doc README.md
%{_sbindir}/%{name}.py


%changelog
* Mon Aug 01 2022 TI_Eugene <tieugene@fedoraproject.org> - 0.0.1-1
- Initial build
