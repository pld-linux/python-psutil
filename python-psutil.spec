#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (some require network)
%bcond_without	python2	# CPython 2.x module
%bcond_with	python3	# CPython 3.x module (see python3-psutil.spec)

%define		module	psutil
Summary:	A cross-platform process and system utilities module for Python
Summary(pl.UTF-8):	Wieloplatformowe narzędzia do procesów i systemu dla Pythona
Name:		python-%{module}
# keep 6.x here for python2 support
Version:	6.1.1
Release:	3
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://pypi.org/simple/psutil/
Source0:	https://github.com/giampaolo/psutil/archive/release-%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	d6738c39444a9218b29dcda0c86d819f
URL:		https://github.com/giampaolo/psutil
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with python2}
BuildRequires:	python-devel >= 1:2.7
%if %{with tests}
BuildRequires:	python-enum34
BuildRequires:	python-futures
BuildRequires:	python-ipaddress
BuildRequires:	python-mock >= 1.0.1
BuildRequires:	python-pytest >= 4.6.11
%endif
%endif
%if %{with python3}
BuildRequires:	python3-devel >= 1:3.6
BuildRequires:	python3-modules >= 1:3.6
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
%if %{with doc}
BuildRequires:	python-sphinx_rtd_theme
BuildRequires:	sphinx-pdg-2
%endif
Requires:	python-modules >= 1:2.7
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
Requires:	python3-modules >= 1:3.6

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
BuildArch:	noarch

%description apidocs
API documentation for Python psutil module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Pythona psutil.

%prep
%setup -q -n %{module}-release-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
cd build-2/lib.*
ln -sf ../../scripts .
ln -sf ../../setup.py .
LC_ALL=C.UTF-8 \
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python} -m psutil.tests
%{__rm} scripts setup.py
%{__rm} -rf .pytest_cache
cd ../..
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
cd build-3/lib.*
ln -sf ../../scripts .
ln -sf ../../setup.py .
PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 \
PYTHONPATH=$(pwd) \
%{__python3} -m psutil.tests
%{__rm} scripts setup.py
%{__rm} -rf .pytest_cache
cd ../..
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
%doc CREDITS HISTORY.rst LICENSE README.rst SECURITY.md
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
%doc docs/_build/html/{_static,*.html,*.js}
%endif
