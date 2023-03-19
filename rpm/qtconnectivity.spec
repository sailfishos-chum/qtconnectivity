%global qt_version 5.15.8

Summary: Qt5 - Connectivity components
Name: opt-qt5-qtconnectivity
Version: 5.15.8
Release: 1%{?dist}

# See LICENSE.GPL3, respectively, for exception details
License: LGPLv2 with exceptions or GPLv3 with exceptions
Url:     http://qt.io
Source0: %{name}-%{version}.tar.bz2

# filter qml provides
%global __provides_exclude_from ^%{_opt_qt5_archdatadir}/qml/.*\\.so$

BuildRequires: make
BuildRequires: opt-qt5-qtbase-devel >= %{qt_version}
BuildRequires: opt-qt5-qtbase-private-devel >= %{qt_version}
%{?_opt_qt5:Requires: %{_opt_qt5}%{?_isa} = %{_opt_qt5_version}}
BuildRequires: opt-qt5-qtdeclarative-devel >= %{qt_version}
BuildRequires: pkgconfig(bluez)

%description
%{summary}.

%package devel
Summary: Development files for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: opt-qt5-qtbase-devel%{?_isa}
%description devel
%{summary}.

%package examples
Summary: Programming examples for %{name}
Requires: %{name}%{?_isa} = %{version}-%{release}
%description examples
%{summary}.


%prep
%autosetup -n %{name}-%{version}/upstream -p1


%build
export QTDIR=%{_opt_qt5_prefix}
touch .git

%{opt_qmake_qt5}

%make_build


%install
make install INSTALL_ROOT=%{buildroot}

%if 0%{?docs}
make install_docs INSTALL_ROOT=%{buildroot}
%endif

## .prl/.la file love
# nuke .prl reference(s) to %%buildroot, excessive (.la-like) libs
pushd %{buildroot}%{_opt_qt5_libdir}
for prl_file in libQt5*.prl ; do
  sed -i -e "/^QMAKE_PRL_BUILD_DIR/d" ${prl_file}
  if [ -f "$(basename ${prl_file} .prl).so" ]; then
    rm -fv "$(basename ${prl_file} .prl).la"
    sed -i -e "/^QMAKE_PRL_LIBS/d" ${prl_file}
  fi
done
popd


%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig


%files
%license LICENSE.GPL* LICENSE.LGPL*
%{_opt_qt5_bindir}/sdpscanner
%{_opt_qt5_libdir}/libQt5Bluetooth.so.5*
%{_opt_qt5_archdatadir}/qml/QtBluetooth/
%{_opt_qt5_libdir}/libQt5Nfc.so.5*
%{_opt_qt5_archdatadir}/qml/QtNfc/

%files devel
%{_opt_qt5_headerdir}/QtBluetooth/
%{_opt_qt5_libdir}/libQt5Bluetooth.so
%{_opt_qt5_libdir}/libQt5Bluetooth.prl
%dir %{_opt_qt5_libdir}/cmake/Qt5Bluetooth/
%{_opt_qt5_libdir}/cmake/Qt5Bluetooth/Qt5BluetoothConfig*.cmake
%{_opt_qt5_libdir}/pkgconfig/Qt5Bluetooth.pc
%{_opt_qt5_archdatadir}/mkspecs/modules/qt_lib_bluetooth*.pri
%{_opt_qt5_headerdir}/QtNfc/
%{_opt_qt5_libdir}/libQt5Nfc.so
%{_opt_qt5_libdir}/libQt5Nfc.prl
%dir %{_opt_qt5_libdir}/cmake/Qt5Nfc/
%{_opt_qt5_libdir}/cmake/Qt5Nfc/Qt5NfcConfig*.cmake
%{_opt_qt5_libdir}/pkgconfig/Qt5Nfc.pc
%{_opt_qt5_archdatadir}/mkspecs/modules/qt_lib_nfc*.pri
