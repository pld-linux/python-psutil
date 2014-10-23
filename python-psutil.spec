#
# Conditional build:
%bcond_without	tests	# do not perform "make test"
%bcond_without  python2 # CPython 2.x module
%bcond_without  python3 # CPython 3.x module

%define 	module	psutil
Summary:	A cross-platform process and system utilities module for Python
Summary(pl.UTF-8):	Wieloplatformowe narzędzia do procesów i systemu dla Pythona
Name:		python-%{module}
Version:	2.1.3
Release:	1
License:	BSD
Group:		Development/Languages/Python
Source0:	https://pypi.python.org/packages/source/p/psutil/%{module}-%{version}.tar.gz
# Source0-md5:	015a013c46bb9bc30b5c344f26dea0d3
URL:		http://code.google.com/p/psutil/
BuildRequires:	rpm-pythonprov
%if %{with python2}
BuildRequires:	python-devel
BuildRequires:	python-distribute
%endif
%if %{with python3}
BuildRequires:	python3-devel
BuildRequires:	python3-distribute
BuildRequires:	python3-modules
%endif
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

%package -n python3-%{module}
Summary:	A cross-platform process and system utilities module for Python
Summary(pl.UTF-8):	Wieloplatformowe narzędzia do procesów i systemu dla Pythona
Group:		Libraries/Python
Requires:	python3-modules

%description -n python3-%{module}
Module providing an interface for retrieving information on all
running processes and system utilization (CPU, disk, memory, network)
in a portable way by using Python, implementing many functionalities
offered by command line tools.

%description -n python3-%{module} -l pl.UTF-8
Module providing an interface for retrieving information on all
running processes and system utilization (CPU, disk, memory, network)
in a portable way by using Python, implementing many functionalities
offered by command line tools.

%prep
%setup -q -n %{module}-%{version}

%build
%if %{with python2}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__python} setup.py build --build-base build-2
%{?with_tests:export PYTHONPATH=$(pwd)/build-2; %{__python} setup.py test}
%endif

%if %{with python3}
CC="%{__cc}" \
CFLAGS="%{rpmcppflags} %{rpmcflags}" \
%{__python3} setup.py build --build-base build-3
%{?with_tests:export PYTHONPATH=$(pwd)/build-3; %{__python3} setup.py test}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%{__python} setup.py \
        build --build-base build-2 \
        install --skip-build \
        --optimize=2 \
        --root=$RPM_BUILD_ROOT

%py_postclean
%endif

%if %{with python3}
%{__python3} setup.py \
        build --build-base build-3 \
        install --skip-build \
        --optimize=2 \
        --root=$RPM_BUILD_ROOT
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -a examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
        | xargs sed -i '1s|^#!.*python\b|#!%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CREDITS README.rst HISTORY.rst

%{py_sitedir}/%{module}
%attr(755,root,root) %{py_sitedir}/_psutil_linux.so
%attr(755,root,root) %{py_sitedir}/_psutil_posix.so

%if "%{py_ver}" > "2.4"
%{py_sitedir}/%{module}-*.egg-info
%endif
%{_examplesdir}/%{name}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CREDITS README.rst HISTORY.rst

%{py3_sitedir}/%{module}
%attr(755,root,root) %{py3_sitedir}/_psutil_linux.*.so
%attr(755,root,root) %{py3_sitedir}/_psutil_posix.*.so

%{py3_sitedir}/%{module}-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif
