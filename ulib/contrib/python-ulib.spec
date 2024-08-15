%global module ulib
Name:		python-%{module}
Version:	0.0.2
Release:	1%{?dist}
License:	GLPv3
Summary:	uLib
URL:		https://github.com/tieugene/utools
Source0:	%{module}-%{version}.tar.gz
BuildArch:	noarch
BuildRequires:  pyproject-rpm-macros
# python3-wheel
BuildRequires:	%{py3_dist wheel}
# python3-sh
BuildRequires:	%{py3_dist sh}
BuildRequires:	python3-libmount
# python3-libvirt
BuildRequires:	%{py3_dist libvirt-python}

%description
%{summary}.


%package -n python3-%{module}
Summary:	%{summary}
%{?python_provide:%python_provide python3-%{module}}

%description -n python3-%{module}
%{summary}.


%prep
%autosetup -n %{module}-%{version}
%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files %{module}


%files -n python3-%{module} -f %{pyproject_files}
%doc README.md
%license LICENSE
%{_bindir}/%{module}


%changelog
* Wed Aug 14 2024 TI_Eugene <ti.eugene@gmail.com> - 0.0.2-1
- Initial packaging
