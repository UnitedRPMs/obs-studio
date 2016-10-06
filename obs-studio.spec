#globals for obs-studio-0.14.2-20160618-e3deb71.tar
%global gitdate 20161006
%global commit0 986edc84c4daff1852b94d1b7557f299ff54504c
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})

Summary: Open Broadcaster Software Studio
Name: obs-studio
Version: 0.16.2
Release: 1.%{gitdate}git%{shortcommit0}%{dist}
Group: Applications/Multimedia
URL: https://obsproject.com/
License: GPLv2+ 
Source0:  https://github.com/jp9000/%{name}/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
BuildRequires: cmake 
BuildRequires: gcc 
BuildRequires: gcc-c++
BuildRequires: gcc-objc 
BuildRequires: pkgconfig 
BuildRequires: ffmpeg-devel 
BuildRequires: jansson-devel 
BuildRequires: pulseaudio-libs-devel
BuildRequires: jack-audio-connection-kit-devel 
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
BuildRequires: faac-devel
BuildRequires: ImageMagick-devel
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: systemd-devel
BuildRequires:  doxygen 
Requires:      ffmpeg x264

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
%autosetup -n %{name}-%{commit0}

#patch -p0
# rpmlint reports E: hardcoded-library-path
# replace OBS_MULTIARCH_SUFFIX by LIB_SUFFIX
sed -i 's|OBS_MULTIARCH_SUFFIX|LIB_SUFFIX|g' cmake/Modules/ObsHelpers.cmake

%build
#export CPPFLAGS=-DFFMPEG_MUX_FIXED=%{_libexecdir}/obs-plugins/obs-ffmpeg/ffmpeg-mux
%cmake -DOBS_VERSION_OVERRIDE=%{version} -DUNIX_STRUCTURE=1
%make_build

%install
%make_install

#mkdir -p %{buildroot}/%{_libexecdir}/obs-plugins/obs-ffmpeg/
#mv -f %{buildroot}/%{_datadir}/obs/obs-plugins/obs-ffmpeg/ffmpeg-mux %{buildroot}/%{_libexecdir}/obs-plugins/obs-ffmpeg/ffmpeg-mux
#ln -sf %{_libexecdir}/obs-plugins/obs-ffmpeg/ffmpeg-mux %{buildroot}/%{_datadir}/obs/obs-plugins/obs-ffmpeg/ffmpeg-mux

%check
desktop-file-validate %{buildroot}%{_datadir}/applications/obs.desktop

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
%doc README
%license COPYING
%{_bindir}/obs
%{_datadir}/applications/obs.desktop
%{_datadir}/icons/hicolor/256x256/apps/obs.png
%{_datadir}/obs/
#%{_libexecdir}/obs-plugins/obs-ffmpeg/ffmpeg-mux

%files libs
%{_libdir}/obs-plugins/
%{_libdir}/*.so.*

%files devel
%{_libdir}/cmake/LibObs/
%{_libdir}/*.so
%{_includedir}/obs/

%changelog
* Thu Oct 06 2016 Pavlo Rudyi <paulcarroty at riseup.net> - 0.16.2-1
- Update to 0.16.2

* Tue Aug 16 2016 Pavlo Rudyi <paulcarroty at riseup.net> - 0.15.4-1 
- Update to 0.15.4

* Fri Jul 22 2016 Pavlo Rudyi <paulcarroty at riseup net> - 0.15.2-1
- Update to 0.15.2 

* Thu Jul 07 2016 David Vásquez <davidjeremias82 AT gmail DOT com> 0.14.2-6.20160618gite3deb7
- Rebuilt for FFmpeg 3.1 

* Sun Jun 26 2016 The UnitedRPMs Project (Key for UnitedRPMs infrastructure) <unitedrpms@protonmail.com> - 0.14.2-5.20160618gite3deb71
- Rebuild with new ffmpeg

* Thu Jun 23 2016 Pavlo Rudyi <paulcarroty at riseup net> - 0.14.2-4-20160618gite3deb71
- Add faac-devel depends for recording crash

* Mon Jun 20 2016 Pavlo Rudyi <paulcarroty at riseup net> - 0.14.2-3-20160618gite3deb71
- Include the previos changes by Sergio Basto

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

