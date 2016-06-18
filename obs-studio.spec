
%global gitdate 20160617
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
Patch: obs-ffmpeg-mux.patch

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
%patch -p0

%build
export CPPFLAGS=-DFFMPEG_MUX_FIXED=\"%{_libexecdir}/obs-plugins/obs-ffmpeg/ffmpeg-mux\"
%cmake -DOBS_VERSION_OVERRIDE=%{version} -DUNIX_STRUCTURE=1
%make_build

%install
%make_install
%ifarch x86_64
mkdir %{buildroot}/%{_libdir}
mv %{buildroot}/%{_libdir}/../lib/*.so %{buildroot}/%{_libdir}
mv %{buildroot}/%{_libdir}/../lib/*.so.* %{buildroot}/%{_libdir}
%endif

mkdir -p %{buildroot}/%{_libexecdir}/obs-plugins/obs-ffmpeg/
mv -f %{buildroot}/%{_datadir}/obs/obs-plugins/obs-ffmpeg/ffmpeg-mux %{buildroot}/%{_libexecdir}/obs-plugins/obs-ffmpeg/ffmpeg-mux

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
%{_libexecdir}/obs-plugins/obs-ffmpeg/ffmpeg-mux

%files libs
%{_libdir}/../lib/obs-plugins/
%{_libdir}/*.so.*

%files devel
%{_libdir}/../lib/cmake/LibObs/
%{_libdir}/*.so
%{_includedir}/obs/

%changelog
* Fri Jun 17 2016 Pavlo Rudyi <paulcarroty at riseup net> - 0.14.2-1.20160617gite3deb71
- update to 14.2
- change version according to Fedora Package Naming Guidelines
- use the macros in %prep

* Mon May 02 2016 David Vasquez <davidjeremias82 at gmail dot com> - 0.14.1-20160502-3cb36bb-2
- Fixed Shared libraries
- Added desktop-file-validate check
- Fixed arch-dependent-file-in-usr-share

* Tue Apr 26 2016 Yiwan <caoli5288@gmail.com> - 0.14.1-1
- Updated to 0.14.1

