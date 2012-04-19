#
# Conditional build:
%bcond_without	tests	# do not perform "make test"

%define 	module	psutil
Summary:	A cross-platform process and system utilities module for Python
Summary(pl.UTF-8):	Wieloplatformowe narzędzia do procesów i systemu dla Pythona
Name:		python-%{module}
Version:	0.4.1
Release:	0.1
License:	BSD
Group:		Development/Languages/Python
Source0:	http://psutil.googlecode.com/files/%{module}-%{version}.tar.gz
# Source0-md5:	9dbefbc6c71f5e50a17a70b18c1150b0
URL:		http://code.google.com/p/psutil/
BuildRequires:	python-devel
BuildRequires:	python-distribute
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Module providing an interface for retrieving information on all
running processes and system utilization (CPU, disk, memory, network)
in a portable way by using Python, implementing many functionalities
offered by command line tools.

%description -l pl.UTF-8
Moduł dostarczający interfejs do informacji o działających procesach
oraz zużyciu systemu (procesor, dyski, pamięć, sieć) w przenośny
sposób używjąc Pythona. Implementuje wiele funkcjonalności oferowanych
przez narzędzia linii komend.

%prep
%setup -q -n %{module}-%{version}


%build
CC="%{__cc}" \
CFLAGS="%{rpmcflags}" \
%{__python} setup.py build

%{?with_tests:%{__python} setup.py test}

%install
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install \
	--skip-build \
	--optimize=2 \
	--root=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%py_ocomp $RPM_BUILD_ROOT%{py_sitedir}
%py_comp $RPM_BUILD_ROOT%{py_sitedir}
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc CREDITS README

%{py_sitedir}/%{module}
%attr(755,root,root) %{py_sitedir}/_psutil_linux.so
%attr(755,root,root) %{py_sitedir}/_psutil_posix.so

%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
