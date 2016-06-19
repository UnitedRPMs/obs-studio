#globals for obs-studio-0.14.2-20160618-e3deb71.tar
%global gitdate 20160618
%global gitversion e3deb71
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}

Summary: Open Broadcaster Software Studio
Name: obs-studio
Version: 0.14.2
Release: 1%{?gver}%{dist}
Group: Applications/Multimedia
URL: https://obsproject.com/
License: GPLv2+ 
Source: %{name}-%{version}-%{snapshot}.tar
Source1: %{name}-snapshot.sh
# Patch: obs-ffmpeg-mux.patch

BuildRequires: cmake 
BuildRequires: gcc 
BuildRequires: gcc-c++ 
BuildRequires: pkgconfig 
BuildRequires: ffmpeg-devel 
BuildRequires: jansson-devel 
BuildRequires: pulseaudio-libs-devel 
BuildRequires: qt5-qtbase-devel 
BuildRequires: qt5-qtx11extras-devel 
BuildRequires: zlib-devel 
BuildRequires: mesa-libGL-devel 
BuildRequires: libXext-devel 
BuildRequires: libxcb-devel 
BuildRequires: libX11-devel 
BuildRequires: libcurl-devel 
BuildRequires: libv4l-devel 
BuildRequires: x264-devel 
BuildRequires: git
BuildRequires: desktop-file-utils
BuildRequires: libXcomposite-devel
BuildRequires: libXinerama-devel
BuildRequires: libXrandr-devel
BuildRequires: fdk-aac-devel
BuildRequires: ImageMagick-devel
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel

%package libs
Summary: Open Broadcaster Software Studio libraries

%package devel
Summary: Open Broadcaster Software Studio header files

%description
Open Broadcaster Software is free and open source
software for video recording and live streaming.

%description libs
Library files for Open Broadcaster Software

%description devel
Header files for Open Broadcaster Software

%prep
%setup -n %{name}-%{version}

%build
cmake -DCMAKE_INSTALL_PREFIX=/usr \
%ifarch x86_64 
      -DOBS_MULTIARCH_SUFFIX=64 \
%endif
      -DOBS_VERSION_OVERRIDE=%{version} .

make %{?_smp_mflags}

%install
%make_install

%check
desktop-file-validate %{buildroot}/%{_datadir}/applications/obs.desktop

%post
update-desktop-database >&/dev/null || :
touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
update-desktop-database >&/dev/null || :
if [ $1 -eq 0 ]; then
 touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
 gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi

%post libs -p /sbin/ldconfig

%postun libs -p /sbin/ldconfig

%posttrans
gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%files
%doc README COPYING
%{_bindir}/obs
%{_datadir}/applications/obs.desktop
%{_datadir}/icons/hicolor/256x256/apps/obs.png
%{_datadir}/obs/

%files libs
%{_libdir}/obs-plugins/
%{_libdir}/*.so.*

%files devel
%{_libdir}/cmake/LibObs/
%{_libdir}/*.so
%{_includedir}/obs/

%changelog

* Sat Jun 18 2016 David Vasquez <davidjeremias82 at gmail dot com> - 0.14.2-2-20160618gite3deb71
- Enabled linux-capture
- Enabled fdk
- Enabled Imagemagick
- Enabled Multiarch Suffix

* Fri Jun 17 2016 Pavlo Rudyi <paulcarroty at riseup net> - 0.14.2-1.20160617gite3deb71
- update to 14.2
- change version according to Fedora Package Naming Guidelines
- use the macros in %prep

* Mon May 02 2016 David Vasquez <davidjeremias82 at gmail dot com> - 0.14.1-2-20160502-3cb36bb
- Fixed Shared libraries
- Added desktop-file-validate check
- Fixed arch-dependent-file-in-usr-share

* Tue Apr 26 2016 Yiwan <caoli5288@gmail.com> - 0.14.1-1
- Updated to 0.14.1

* Thu Sep 24 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.12.0-0.1
- Updated to 0.12.0

* Mon Aug 17 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.11.4-0.1
- Added OBS_VERSION_OVERRIDE to correct version in compilation
- Updated to 0.11.4

* Sat Aug 08 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.11.3-0.1
- Updated to 0.11.3

* Thu Jul 30 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.11.2-0.1
- Updated to 0.11.2

* Fri Jul 10 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.11.1-0.1
- Updated to 0.11.1

* Wed May 27 2015 Momcilo Medic <fedorauser@fedoraproject.org> - 0.10.1-0.1
- Initial .spec file

