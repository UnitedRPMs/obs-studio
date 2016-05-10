#globals for obs-studio-0.14.1-20160502-3cb36bb.tar
%global gitdate 20160502
%global commit1 3cb36bbd5154163a442915f703002d4b0ce16f84
%global gitversion %(c=%{commit1}; echo ${c:0:7})
%global snapshot %{gitdate}-%{gitversion}
%global gver .%{gitdate}git%{gitversion}

Name:           obs-studio
Version:        0.14.1
Release:        2%{?gver}%{dist}
Summary:        Open Broadcaster Software Studio
Group:          Applications/Multimedia
License:        GPLv2+
URL:            https://obsproject.com/
Source:         https://github.com/jp9000/%{name}/archive/%{commit1}.tar.gz#/%{name}-%{version}-%{snapshot}.tar.gz
Patch:          obs-ffmpeg-mux.patch

BuildRequires:  desktop-file-utils

BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  cmake
BuildRequires:  libX11-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  ffmpeg-devel
BuildRequires:  libv4l-devel
BuildRequires:  pulseaudio-libs-devel
BuildRequires:  x264-devel
BuildRequires:  zlib-devel
BuildRequires:  libXext-devel
BuildRequires:  libxcb-devel
BuildRequires:  libcurl-devel
BuildRequires:  qt5-qtbase-devel
BuildRequires:  qt5-qtx11extras-devel
BuildRequires:  jansson-devel
#BuildRequires:  git
#BuildRequires:  pkgconfig

%package libs
Summary:        Open Broadcaster Software Studio libraries

%package devel
Summary:        Open Broadcaster Software Studio header files

%description
Open Broadcaster Software is free and open source
software for video recording and live streaming.

%description libs
Library files for Open Broadcaster Software

%description devel
Header files for Open Broadcaster Software


%prep
%setup -qn obs-studio-%{commit1}
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

* Mon May 02 2016 David Vasquez <davidjeremias82 at gmail dot com> - 0.14.1-20160502-3cb36bb-2
- Fixed Shared libraries
- Added desktop-file-validate check
- Fixed arch-dependent-file-in-usr-share

* Tue Apr 26 2016 Yiwan <caoli5288@gmail.com> - 0.14.1-1
- Updated to 0.14.1

