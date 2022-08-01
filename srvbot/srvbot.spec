Name:           srvbot
Version:        0.0.3
Release:        1%{?dist}
License:        GPLv3
Summary:        Vhost telebot
URL:            https://github.com/tieugene/utools/%{name}
Source0:        %{name}-%{version}.tar.xz
BuildRequires:  systemd-rpm-macros
BuildRequires:  gettext
Requires:       python3 >= 3.6
Requires:       systemd
Requires:       %{py3_dist pytelegrambotapi}
#Requires:       #{py3_dist utools}
BuildArch:      noarch

%description
Telegram bot to control KVM guest.


%prep
%autosetup


%install
%{__install} -Dpm 0755 %{name}.py %{buildroot}%{_sbindir}/%{name}.py
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
%{_sbindir}/%{name}.py
%{_unitdir}/%{name}.service
%{_datadir}/locale/*/LC_MESSAGES/%{name}.mo


%changelog
* Mon Aug 01 2022 TI_Eugene <tieugene@fedoraproject.org> - 0.0.3-1
- Initial build
