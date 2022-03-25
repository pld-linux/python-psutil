# TODO:
# - Fix tests (a few fail)
#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests
%bcond_without	python2	# CPython 2.x module
%bcond_without	python3	# CPython 3.x module

%define		module	psutil
Summary:	A cross-platform process and system utilities module for Python
Summary(pl.UTF-8):	Wieloplatformowe narzędzia do procesów i systemu dla Pythona
Name:		python-%{module}
Version:	5.9.0
Release:	3
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/psutil/
Source0:	https://github.com/giampaolo/psutil/archive/release-%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	080d75a78be3ef1ce72c39a9b001197d
URL:		https://github.com/giampaolo/psutil
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel >= 1:2.6
%if %{with tests}
BuildRequires:	python-ipaddress
BuildRequires:	python-mock
%if "%{py_ver}" < "2.7"
BuildRequires:	python-unittest2
%endif
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.4
BuildRequires:	python3-modules >= 1:3.4
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
Requires:	python3-modules >= 1:3.4

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

%package apidocs
Summary:	API documentation for Python psutil module
Summary(pl.UTF-8):	Dokumentacja API modułu Pythona psutil
Group:		Documentation

%description apidocs
API documentation for Python psutil module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona psutil.

%prep
%setup -q -n %{module}-release-%{version}

%if %{with tests}
# prepare subdir to run tests from
# (cannot use topdir with PYTHONPATH=build-?/lib.* because python finds psutil dir without
# _psutil_linux module inside in cwd before build-?/lib.*/psutil dir from PYTHONPATH)
install -d tests
ln -sf ../scripts tests
ln -sf ../setup.py tests
%endif

%build
%if %{with python2}
%py_build

%if %{with tests}
cd tests
ln -snf ../build-2/lib.*/psutil psutil
PYTHONPATH=$(pwd) \
%{__python} psutil/tests/__main__.py
cd ..
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
cd tests
ln -snf ../build-3/lib.*/psutil psutil
PYTHONPATH=$(pwd) \
%{__python3} psutil/tests/__main__.py
cd ..
%endif
%endif

%if %{with doc}
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-2
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
%doc CREDITS HISTORY.rst LICENSE README.rst
%dir %{py_sitedir}/psutil
%attr(755,root,root) %{py_sitedir}/psutil/_psutil_linux.so
%attr(755,root,root) %{py_sitedir}/psutil/_psutil_posix.so
%{py_sitedir}/psutil/*.py[co]
%{py_sitedir}/psutil-%{version}-py*.egg-info
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc CREDITS HISTORY.rst LICENSE README.rst
%dir %{py3_sitedir}/psutil
%attr(755,root,root) %{py3_sitedir}/psutil/_psutil_linux.*.so
%attr(755,root,root) %{py3_sitedir}/psutil/_psutil_posix.*.so
%{py3_sitedir}/psutil/*.py
%{py3_sitedir}/psutil/__pycache__
%{py3_sitedir}/psutil-%{version}-py*.egg-info
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_modules,_static,*.html,*.js}
%endif
