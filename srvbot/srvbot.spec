Name:           srvbot
Version:        0.0.3
Release:        1%{?dist}
License:        GPLv3
Summary:        Vhost telebot
URL:            https://github.com/tieugene/utools/%{name}
Source0:        %{name}-%{version}.tar.xz
BuildRequires:  python3-setuptools
BuildRequires:  python3-rpm-macros
BuildRequires:  systemd-rpm-macros
BuildRequires:  gettext
Requires:       python3 >= 3.6
Requires:       systemd
Requires:       %{py3_dist pytelegrambotapi}
Requires:       %{py3_dist libvirt-python}
Requires:       %{py3_dist ulib}
BuildArch:      noarch

%description
Telegram bot to control KVM guest.


%prep
%autosetup


%build
%{py3_build}


%install
%{py3_install}
%{__install} -Dpm 0644 %{name}.service %{buildroot}%{_unitdir}/%{name}.service
for lang in $(ls locale)
do
  mkdir -p %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES
  msgfmt -o %{buildroot}%{_datadir}/locale/$lang/LC_MESSAGES/%{name}.mo locale/$lang/LC_MESSAGES/%{name}.po
done


%post
%systemd_post %{name}.service


%preun
%systemd_preun %{name}.service


%postun
%systemd_postun_with_restart %{name}.service


%files
#license LICENSE
%doc README.md srvbot.venv.service
%{_bindir}/%{name}
%{python3_sitelib}/%{name}.py
%{python3_sitelib}/__pycache__/*
%{python3_sitelib}/%{name}-%{version}-py3.*.egg-info/
%{_unitdir}/%{name}.service
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo


%changelog
* Tue Aug 02 2022 TI_Eugene <tieugene@fedoraproject.org> - 0.0.3-1
- Initial build
