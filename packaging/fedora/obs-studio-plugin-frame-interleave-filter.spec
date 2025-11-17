Name: obs-studio-plugin-frame-interleave-filter
Version: @VERSION@
Release: @RELEASE@%{?dist}
Summary: Interleaves video frames in OBS Studio
License: GPLv2+

Source0: %{name}-%{version}.tar.bz2
BuildRequires: cmake, gcc, gcc-c++
BuildRequires: obs-studio-devel

%description
This plugin interleaves video frames to reduce CPU and GPU usage.

%prep
%autosetup -p1
sed -i -e 's/project(obs-frame-interleave-filter/project(frame-interleave-filter/g' CMakeLists.txt

%build
%{cmake} -DLINUX_PORTABLE=OFF -DLINUX_RPATH=OFF -DQT_VERSION=6 -DINSTALL_LICENSE_FILES:BOOL=OFF
%{cmake_build}

%install
%{cmake_install}

%files
%{_libdir}/obs-plugins/*.so
%{_datadir}/obs/obs-plugins/*/
%license LICENSE
