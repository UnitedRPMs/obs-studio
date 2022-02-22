%global commit0 acad9dbaf7bcf8f567c3e5c613411ca04ba92fa9
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global gver .git%{shortcommit0}


%define _legacy_common_support 1
%global _hardened_build 1
%define debug_package %{nil}

# Reduce compression level and build time
%define _source_payload w5.gzdio
%define _binary_payload w5.gzdio

# Plugins

# https://github.com/exeldro/obs-move-transition/releases
%global mv_tra 2.5.7

# https://github.com/sorayuki/obs-multi-rtmp
%global mt_rtmp 0.2.8

# https://github.com/Qufyy/obs-scale-to-sound
%global os_ts 1.2.0

# https://github.com/Xaymar/obs-StreamFX
%global commit1 1b80a1485cb85129fbebd60596d250e7d2162bfa
%global shortcommit1 %(c=%{commit1}; echo ${c:0:7})
%global gver .git%{shortcommit1}

# https://github.com/exeldro/obs-downstream-keyer
%global commit2 9d5b21ba49f2853004755c654af5bc708c796982
%global shortcommit2 %(c=%{commit2}; echo ${c:0:7})
%global gver .git%{shortcommit2}

# https://github.com/exeldro/obs-time-warp-scan
%global commit3 630637ea3a5768e99dd43c772fb0e6766406717b
%global shortcommit3 %(c=%{commit3}; echo ${c:0:7})
%global gver .git%{shortcommit3}

# https://github.com/obsproject/obs-vst/
%global commit4 8ad3f64e702ac4f1799b209a511620eb1d096a01
%global shortcommit4 %(c=%{commit4}; echo ${c:0:7})

Summary: Open Broadcaster Software Studio
Name: obs-studio
Version: 27.2.1
Release: 7%{gver}%{dist}
Group: Applications/Multimedia
URL: https://obsproject.com/
License: GPLv2+ 
Source0:  https://github.com/obsproject/obs-studio/archive/%{commit0}.tar.gz#/%{name}-%{shortcommit0}.tar.gz
Source1:  obs-studio-snapshot
Source2:  https://github.com/obsproject/obs-vst/archive/%{commit4}/obs-vst-%{shortcommit4}.tar.gz
Source3:  https://github.com/exeldro/obs-move-transition/archive/refs/tags/%{mv_tra}.tar.gz#/obs-move-transition-%{mv_tra}.tar.gz
Source4:  https://github.com/Xaymar/obs-StreamFX/archive/%{commit1}.zip#/obs-StreamFX-%{shortcommit1}.tar.gz
Source5:  https://github.com/exeldro/obs-downstream-keyer/archive/%{commit2}.zip#/obs-downstream-keyer-%{shortcommit2}.tar.gz
Source6:  https://github.com/exeldro/obs-time-warp-scan/archive/%{commit3}.zip#/obs-time-warp-scan-%{shortcommit3}.tar.gz
Source11:  https://github.com/Qufyy/obs-scale-to-sound/archive/refs/tags/%{os_ts}.zip#/obs-scale-to-sound-%{os_ts}.tar.gz

# obs-StreamFX/third-party/
Source7:  obs-streamfx-snapshot

Patch:    plugins.patch

BuildRequires: cmake3 
BuildRequires: ninja-build
BuildRequires: gcc 
BuildRequires: gcc-c++
BuildRequires: gcc-objc 
BuildRequires: pkgconfig 
BuildRequires: ffmpeg4-devel  
BuildRequires: fdk-aac-free-devel
BuildRequires: nvenc
BuildRequires: nv-codec-headers srt-devel svt-av1-devel
BuildRequires: jansson-devel 
BuildRequires: wayland-devel
BuildRequires: qt5-qtbase-private-devel
BuildRequires: qt5-qtsvg-devel
BuildRequires: qt5-qtwayland-devel
%if 0%{?fedora} >= 34
BuildRequires: pkgconfig(libpipewire-0.3)
%endif
BuildRequires: libsndfile
BuildRequires: flac-libs
BuildRequires: jack-audio-connection-kit-devel 
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
BuildRequires: luajit-devel
BuildRequires: x264-devel >= 1:0.161
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
BuildRequires: pkgconfig(xkbcommon)
BuildRequires: pkgconfig(libpci)
BuildRequires: jansson-devel
BuildRequires: swig
BuildRequires: speexdsp-devel
BuildRequires: doxygen
BuildRequires: make
BuildRequires: unzip
BuildRequires: libaom-devel
BuildRequires: opus
BuildRequires: libogg

# plugins support
BuildRequires: cef-minimal >= 88.2.8
BuildRequires: fdk-aac-free
BuildRequires: vlc-devel
BuildRequires: alsa-lib-devel
BuildRequires: libftl-devel

# new
BuildRequires: automoc
BuildRequires: at-spi2-atk-devel nss-devel libXScrnSaver-devel
BuildRequires: libajantv2

Requires:      %{name}-libs = %{version}-%{release}
Recommends:    v4l2loopback
Recommends:    v4l2loopback-dkms
Recommends:    droidcam-obs-plugin

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
%autosetup -T -D -n %{name}-%{shortcommit0} -p1 -a3

# libobs multilib
sed -i 's|lib/pkgconfig|%{_lib}/pkgconfig|g' libobs/CMakeLists.txt

# Plugins
echo 'add_subdirectory(StreamFX)' >> plugins/CMakeLists.txt
cp -rf obs-move-transition-%{mv_tra} plugins/obs-move-transition
tar -xf %{S:2} -C plugins/obs-vst --strip-components=1
unzip %{S:4} && cp -rf obs-StreamFX-%{commit1} plugins/StreamFX
unzip %{S:6} && cp -rf obs-time-warp-scan-%{commit3}  plugins/time-warp-scan
unzip %{S:11} && cp -rf obs-scale-to-sound-%{os_ts}  plugins/scale-to-sound
unzip %{S:5} && cp -rf obs-downstream-keyer-%{commit2} UI/frontend-plugins/downstream-keyer

# obs-StreamFX/third-party/
%{S:7} -c %{commit1}
rm -rf plugins/StreamFX && mv -f obs-StreamFX-%{shortcommit1} plugins/StreamFX

%build
mkdir -p build

cmake -B build -DCMAKE_INSTALL_PREFIX="/usr" \
 -DCMAKE_INSTALL_LIBDIR=%{_libdir} \
 -DOBS_MULTIARCH_SUFFIX="%(echo %{_lib} | sed -e 's/lib//')" \
 -DCMAKE_AR=%{_bindir}/gcc-ar \
 -DCMAKE_RANLIB=%{_bindir}/gcc-ranlib \
 -DCMAKE_NM=%{_bindir}/gcc-nm \
 -DUNIX_STRUCTURE=ON \
 -DCMAKE_BUILD_TYPE=Release \
 -DCMAKE_VERBOSE_MAKEFILE=OFF \
 -DOBS_VERSION_OVERRIDE=%{version} \
 -DBUILD_BROWSER=ON  \
 -DENABLE_SCRIPTING=OFF \
%if 0%{?fedora} >= 34
 -DENABLE_PIPEWIRE=ON \
 %else
 -DENABLE_PIPEWIRE=OFF \
 %endif
 -DBUILD_VST=ON \
 -DBUILD_CAPTIONS=ON \
 -DCEF_ROOT_DIR="/opt/cef" -Wno-dev 
    
#  -DDISABLE_DECKLINK=ON \  
#  -DOpenGL_GL_PREFERENCE=GLVND \    
# -DLIBOBS_PREFER_IMAGEMAGICK=OFF \        
%make_build -C build


# build docs
#doxygen

%install
%make_install -C build

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
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/apps/*.svg
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

#files doc
#doc docs/html

%changelog

* Tue Feb 22 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.2.1-7.gitacad9db
- Updated to 27.2.1

* Sat Feb 19 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.2-9.git9c504f4
- Updated to 27.2 final release

* Sat Jan 22 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.2-8.git3aa90f7
- Updated to 27.2 Release Candidate 1

* Sat Jan 01 2022 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.2-7.git1dd9612
- Updated to 27.2

* Sun Oct 10 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.1.3-9.git3c14e4e
- Enabled StreamFX and Scale To sound plugin 

* Fri Oct 08 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.1.3-8.git3c14e4e
- Rebuilt

* Wed Oct 06 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.1.3-7.git3c14e4e
- Updated to 27.1.3
- Enabled plugins move-transition, obs-audio-monitor, obs-downstream-keyer and obs-time-warp-scan

* Thu Sep 30 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.1.1-7.git9deb8fe
- Updated to 27.1.1

* Wed Sep 08 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.1.0-7.gite2b7597
- Updated to 27.1.0

* Mon Jun 28 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.0.1-7.gitcd5873e
- Updated to 27.0.1 

* Sun Jun 06 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.0.0-7.git4d647d8
- Updated to 27.0.0 Final release

* Sat Apr 10 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 27.0.0-0.2.git1064cd2
- Updated to 27.0.0 RC1
- Pipeware enabled F34 and Rawhide
- Wayland support

* Mon Jan 11 2021 Unitedrpms Project <unitedrpms AT protonmail DOT com> 26.1.2-7.git2597ed0
- Updated to 26.1.2

* Sun Dec 20 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 26.1.0-8.git38ad3ba
- Updated to stable release

* Fri Nov 27 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 26.1.0-7.git8d58578
- Updated to 26.1.0

* Thu Oct 22 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 26.0.2-9.git3486c0b
- Enabled ftl-sdk plugin missed

* Sat Oct 10 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 26.0.2-7.git3486c0b
- Updated to 26.0.2

* Wed Sep 30 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 26.0.0-4.gite24aaa0
- Updated to stable release

* Mon Sep 21 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 26.0.0-3.git890d325
- Updated to rc3

* Tue Sep 01 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 26.0.0-1.git288a84d
- Updated to 26.0.0

* Mon Aug 03 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 25.0.8-11.git1aee73f
- Rebuilt 

* Sat Jul 04 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 25.0.8-10.git4c0d4a1
- Rebuilt for x264

* Tue Jun 23 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 25.0.8-8.git4c0d4a1
- Rebuilt for ffmpeg

* Mon Apr 27 2020 Unitedrpms Project <unitedrpms AT protonmail DOT com> 25.0.8-7.git4c0d4a1
- Updated to 25.0.8

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
