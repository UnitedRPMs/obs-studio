%global commit0 355cd6ccc0f8435fc1d45043e2ffa1f74ee36b94
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}

%define _legacy_common_support 1
%global _hardened_build 1

Summary: Open Broadcaster Software Studio
Name: obs-studio
Version: 25.0.7
Release: 7%{gver}%{dist}
Group: Applications/Multimedia
URL: https://obsproject.com/
License: GPLv2+ 
Source0:  https://github.com/obsproject/obs-studio/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:  obs-studio-snapshot
Source2:  https://github.com/mixer/ftl-sdk/archive/v0.9.14.tar.gz
BuildRequires: cmake3 
BuildRequires: ninja-build
BuildRequires: gcc 
BuildRequires: gcc-c++
BuildRequires: gcc-objc 
BuildRequires: pkgconfig 
BuildRequires: ffmpeg-devel >= 4.1 
BuildRequires: fdk-aac-free-devel
BuildRequires: nvenc
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
BuildRequires: x264-devel >= 0.157
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
BuildRequires: doxygen 
BuildRequires: mbedtls-devel
BuildRequires: pkgconfig(Qt5Svg)
BuildRequires: libcurl-devel
BuildRequires: jansson-devel
BuildRequires: swig
BuildRequires: speexdsp-devel

# plugins support
BuildRequires: cef-minimal 
BuildRequires: fdk-aac-free
BuildRequires: vlc-devel
BuildRequires: alsa-lib-devel

Requires:      ffmpeg x264
Requires:      %{name}-libs = %{version}-%{release}

%description
Open Broadcaster Software is free and open source
software for video recording and live streaming.

%package libs
Summary: Open Broadcaster Software Studio libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description libs
Library files for Open Broadcaster Software

%package devel
Summary: Open Broadcaster Software Studio header files
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
Header files for Open Broadcaster Software

%package        doc
Summary:        Documentation files for %{name}
Group:          Documentation
BuildArch:      noarch

%description    doc
The %{name}-doc package contains html documentation
that use %{name}.

%prep

# We need some sub-modules
%{S:1} -c %{commit0}
%autosetup -T -D -n %{name}-%{shortcommit0}  

# rpmlint reports E: hardcoded-library-path
# replace OBS_MULTIARCH_SUFFIX by LIB_SUFFIX
sed -i 's|OBS_MULTIARCH_SUFFIX|LIB_SUFFIX|g' cmake/Modules/ObsHelpers.cmake

# libobs multilib
sed -i 's|lib/pkgconfig|%{_lib}/pkgconfig|g' libobs/CMakeLists.txt

#rm -rf plugins/obs-outputs/ftl-sdk 
#tar xmzvf %{S:2} -C plugins/obs-outputs/
#pushd plugins/obs-outputs/
#mv -f ftl-sdk-0.9.14 ftl-sdk
#popd


%build

mkdir build && pushd build
%cmake3 -DBUILD_CAPTIONS=ON -DOBS_VERSION_OVERRIDE=%{version} -DBUILD_BROWSER=ON  -DUNIX_STRUCTURE=1 -DENABLE_SCRIPTING:BOOL=FALSE -DCEF_ROOT_DIR="/opt/cef" -Wno-dev ..       
        
make

popd

# build docs
doxygen

%install
pushd build
%make_install

#mkdir -p %{buildroot}/%{_libexecdir}/obs-plugins/obs-ffmpeg/
#mv -f %{buildroot}/%{_bindir}/obs-ffmpeg-mux \  
#      %{buildroot}/%{_libexecdir}/obs-plugins/obs-ffmpeg/obs-ffmpeg-mux

#check
#/usr/bin/desktop-file-validate %{buildroot}/%{_datadir}/applications/*.desktop

%post
/usr/bin/update-desktop-database >&/dev/null || :
/usr/bin/touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :

%postun
/usr/bin/update-desktop-database >&/dev/null || :
if [ $1 -eq 0 ]; then
  /usr/bin/touch --no-create %{_datadir}/icons/hicolor >&/dev/null || :
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :
fi


%posttrans
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor >&/dev/null || :

%ldconfig_scriptlets libs

%files
%doc README.rst
%license UI/data/license/gplv2.txt
%license COPYING
%{_bindir}/obs
%{_bindir}/obs-ffmpeg-mux
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/256x256/apps/*.png
%{_datadir}/obs/
#{_libexecdir}/obs-plugins/obs-ffmpeg/obs-ffmpeg-mux
%{_datadir}/metainfo/*.appdata.xml

%files libs
%{_libdir}/obs-plugins/
%{_libdir}/*.so.*

%files devel
%{_libdir}/cmake/LibObs/
%{_libdir}/*.so
%{_includedir}/obs/
%{_libdir}/pkgconfig/libobs.pc

%files doc
%doc docs/html

%changelog

* Wed Apr 22 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 25.0.7-7.git355cd6c
- Updated to 25.0.7
- Enabled browser, Vlc and fdk-aac-free plugins

* Wed Apr 15 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 25.0.6-7.gite3c63c0
- Updated 25.0.6

* Thu Apr 09 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 25.0.5-7.gite10d44d
- Updated 25.0.5

* Sun Apr 05 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 25.0.4-7.git47058d9
- Updated 25.0.4

* Mon Mar 23 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 25.0.3-7.git3c78a8a
- Updated 25.0.3

* Thu Mar 19 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 25.0.1-7.gitb19ea6f
- Updated 25.0.1

* Wed Mar 18 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 25.0.0-7.git327a6f5
- Updated 25.0.0

* Fri Dec 20 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 24.0.6-7.git6594d0f
- Updated 24.0.6

* Fri Dec 13 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 24.0.5-7.git99638ba
- Updated 24.0.5

* Fri Dec 06 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 24.0.4-7.git22bddd0
- Updated 24.0.4

* Mon Oct 14 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 24.0.3-7.gitd88a5a5
- Updated 24.0.3

* Tue Oct 01 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 24.0.1-7.git9457047
- Updated 24.0.1

* Sat Jun 15 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 23.2.1-7.git02e523c
- Updated to 23.2.1

* Wed Apr 10 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 23.1.0-7.git6550c0d
- Updated to 23.1.0

* Fri Mar 22 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 23.0.1-8.gitf2d7f5b
- Rebuilt for x264

* Fri Mar 01 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 23.0.1-7.gitf2d7f5b
- Updated to 23.0.1

* Mon Feb 25 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 23.0.0-7.git8181f77
- Updated to 23.0.0

* Thu Jan 03 2019 Unitedrpms Project <unitedrpms AT protonmail DOT com> 22.0.3-8.git7246caa 
- Updated to current commit
- obs-ffmpeg plugin fixed

* Thu Dec 06 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 22.0.3-7.git6523a29  
- Rebuilt for ffmpeg

* Mon Oct 22 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 22.0.3-6.git6523a29  
- Added some plugins missed

* Fri Oct 05 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 22.0.3-5.git6523a29  
- Automatic Mass Rebuild

* Fri Sep 07 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 22.0.3-4.git6523a29  
- Updated to 22.0.3-4.git6523a29

* Mon Aug 27 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 22.0.1-4.git92d7c81  
- Updated to 22.0.1

* Fri Jul 13 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 21.1.2-4.git5dbf8e7  
- Rebuilt for Python 3.7

* Mon May 14 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 21.1.2-3.git5dbf8e7  
- Updated to 21.1.2

* Thu Apr 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> 21.1.1-3.gitfa90926  
- Automatic Mass Rebuild

* Wed Mar 21 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 21.1.1-2.gitfa90926
- Updated to 21.1.1-2.gitfa90926

* Mon Mar 19 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 21.1.0-2.gita81de7f
- Updated to 21.1.0-2.gita81de7f

* Mon Feb 26 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 21.0.3-2.gitaa58b9c
- Updated to 21.0.3-2.gitaa58b9c

* Mon Jan 22 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 21.0.2-2.gitac6b018
- Updated to 21.0.2-2.gitac6b018

* Mon Jan 22 2018 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 21.0.1-2.git4eb5be4
- Updated to 21.0.1-2.git4eb5be4

* Sun Nov 19 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 20.1.3-1.git350e7a7
- Updated to 20.1.3-1.git350e7a7

* Sun Oct 29 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 20.1.1-1.gitbf75619
- Updated to 20.1.1-1.gitbf75619

* Sun Oct 22 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 20.1.0-1.git7bd06e7
- Updated to 20.1.0-1.git7bd06e7

* Wed Oct 18 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> 20.0.1-2.gitd3c163b  
- Automatic Mass Rebuild

* Tue Sep 26 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 20.0.1-1.gitd3c163b
- Updated to 20.0.1-1.gitd3c163b

* Thu Aug 10 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 20.0.0-1.git8b315186
- Updated to 20.0.0-1.git8b315186

* Sat Jul 08 2017 Unitedrpms Project <unitedrpms AT protonmail DOT com> - 19.0.3-1.gitd295ad3
- Updated to 19.0.3-1.gitd295ad3.

* Sat Mar 25 2017 Pavlo Rudyi <paulcarroty at riseup.net> - 18.0.1-1
- Update to 18.0.1

* Sat Mar 18 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 17.0.2-2.20170226gitc8d0893
- Rebuilt for libbluray

* Sun Feb 26 2017 David Vásquez <davidjeremias82 AT gmail DOT com> 17.0.2-1.20170226gitc8d0893
- Updated to 17.0.2-1.20170226gitc8d0893

* Sun Jan 08 2017 Pavlo Rudyi <paulcarroty at riseup.net> - 17.0.0-1
- Update to 17.0.0

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
