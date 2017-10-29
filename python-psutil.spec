# TODO:
# - Fix tests
#
# Conditional build:
%bcond_with	tests	# do not perform "make test"
%bcond_without  python2 # CPython 2.x module
%bcond_without  python3 # CPython 3.x module

%define		module	psutil
Summary:	A cross-platform process and system utilities module for Python
Summary(pl.UTF-8):	Wieloplatformowe narzędzia do procesów i systemu dla Pythona
Name:		python-%{module}
Version:	5.4.0
Release:	1
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.python.org/simple/psutil/
Source0:	https://github.com/giampaolo/psutil/archive/release-%{version}.tar.gz
# Source0-md5:	38c7e18b63ef0af76720a72119f4b2e1
URL:		https://github.com/giampaolo/psutil
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
%if %{with tests}
BuildRequires:	python-mock
%if "%{py_ver}" < "2.7"
BuildRequires:	python-unittest2
%endif
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.2
BuildRequires:	python3-modules >= 1:3.2
%endif
Requires:	python-modules >= 1:2.6
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
Requires:	python3-modules >= 1:3.2

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
%setup -q -n %{module}-release-%{version}

%build
%if %{with python2}
%py_build

%{?with_tests:export PYTHONPATH=$(echo $(pwd)/build-2/lib.*); %{__python} psutil/tests/runner.py}
%endif

%if %{with python3}
%py3_build

%{?with_tests:export PYTHONPATH=$(echo $(pwd)/build-3/lib.*); %{__python3} psutil/tests/runner.py}
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%{__rm} -r $RPM_BUILD_ROOT%{py_sitedir}/psutil/tests
%py_postclean
%endif

%if %{with python3}
%py3_install

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/psutil/tests
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc CREDITS HISTORY.rst IDEAS LICENSE README.rst
%dir %{py_sitedir}/psutil
%attr(755,root,root) %{py_sitedir}/psutil/_psutil_linux.so
%attr(755,root,root) %{py_sitedir}/psutil/_psutil_posix.so
%{py_sitedir}/psutil/*.py[co]
%{py_sitedir}/psutil-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CREDITS HISTORY.rst IDEAS LICENSE README.rst
%dir %{py3_sitedir}/psutil
%attr(755,root,root) %{py3_sitedir}/psutil/_psutil_linux.*.so
%attr(755,root,root) %{py3_sitedir}/psutil/_psutil_posix.*.so
%{py3_sitedir}/psutil/*.py
%{py3_sitedir}/psutil/__pycache__
%{py3_sitedir}/psutil-%{version}-py*.egg-info
%endif
