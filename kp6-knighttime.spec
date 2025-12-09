#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.5.4
%define		qt_ver		6.8.0
%define		kpname		knighttime
Summary:	KNight Time
Name:		kp6-%{kpname}
Version:	6.5.4
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	3650e81d51b072c2d1b1eb4d39adf94b
URL:		http://www.kde.org/
BuildRequires:	Qt6Gui-devel >= %{qt_ver}
BuildRequires:	Qt6Positioning-devel >= %{qt_ver}
BuildRequires:	gettext-tools
BuildRequires:	kf6-extra-cmake-modules >= 6.18.0
BuildRequires:	kf6-kconfig-devel >= 6.18.0
BuildRequires:	kf6-kcoreaddons-devel >= 6.18.0
BuildRequires:	kf6-kdbusaddons-devel >= 6.18.0
BuildRequires:	kf6-kholidays-devel >= 6.18.0
BuildRequires:	kf6-ki18n-devel >= 6.18.0
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The `KNightTime` provides helpers for scheduling the dark-light cycle.
It can be used to implement features such as adjusting the screen
color temperature based on time of day, etc.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%{systemduserunitdir}/plasma-knighttimed.service
%ghost %{_libdir}/libKNightTime.so.0
%{_libdir}/libKNightTime.so.*.*
%attr(755,root,root) %{_prefix}/libexec/knighttimed
%{_desktopdir}/org.kde.knighttimed.desktop
%{_datadir}/dbus-1/interfaces/org.kde.NightTime.xml
%{_datadir}/dbus-1/services/org.kde.NightTime.service
%{_datadir}/qlogging-categories6/knighttime.categories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KNightTime
%{_libdir}/cmake/KNightTime
%{_libdir}/libKNightTime.so

