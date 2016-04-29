Summary: Open Broadcaster Software Studio
Name: obs-studio
Version: 0.14.1
Release: 1%{?dist}

URL: https://obsproject.com/
License: GPLv2+ 
Source: %{name}-%{version}.tar.gz

BuildRequires: cmake gcc gcc-c++ pkgconfig ffmpeg-devel jansson-devel pulseaudio-libs-devel qt5-qtbase-devel qt5-qtx11extras-devel zlib-devel mesa-libGL-devel libXext-devel libxcb-devel libX11-devel libcurl-devel libv4l-devel x264-devel

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
%setup -q

%build
%cmake -DOBS_VERSION_OVERRIDE=%{version}
%make_build

%install
%make_install
%ifarch x86_64
mkdir %buildroot%_libdir
mv %buildroot%_libdir/../lib/*.so %buildroot%_libdir
mv %buildroot%_libdir/../lib/*.so.* %buildroot%_libdir
%endif

%post
/sbin/ldconfig
update-desktop-database >&/dev/null || :
touch --no-create %_datadir/icons/hicolor >&/dev/null || :

%postun
/sbin/ldconfig
update-desktop-database >&/dev/null || :
if [ $1 -eq 0 ]; then
 touch --no-create %_datadir/icons/hicolor >&/dev/null || :
 gtk-update-icon-cache %_datadir/icons/hicolor >&/dev/null || :
fi

%posttrans
gtk-update-icon-cache %_datadir/icons/hicolor >&/dev/null || :

%files
%_bindir/obs
%_datadir/applications/obs.desktop
%_datadir/icons/hicolor/256x256/apps/obs.png
%_datadir/obs/
%doc README COPYING

%files libs
%_libdir/../lib/obs-plugins/
%_libdir/*.so.*

%files devel
%_libdir/../lib/cmake/LibObs/
%_libdir/*.so
%_includedir/obs/

%changelog
* Tue Apr 26 2016 Yiwan <caoli5288@gmail.com> - 0.14.1-1
- Updated to 0.14.1

