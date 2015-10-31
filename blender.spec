# TODO:
# - enable internalization support (BR libftgl)
# - libsolid/libqhull/libode BR ?
Summary:	3D modeling, rendering, animation and game creation package
Summary(pl.UTF-8):	Pakiet do tworzenia animacji 3D oraz gier
Name:		blender
Version:	2.76
Release:	3
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://download.blender.org/source/%{name}-%{version}.tar.gz
# Source0-md5:	1f35ae56bb221bbeb21e89501fbd6c6a
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:	%{name}.manpage
Patch0:		%{name}-2.76-droid.patch
URL:		http://www.blender.org/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenImageIO-devel
BuildRequires:	SDL2-devel
BuildRequires:	cmake
#BuildRequires:	esound-devel
BuildRequires:	ffmpeg-devel >= 0.4.9-4.20080930.1
BuildRequires:	freealut-devel
BuildRequires:	freetype-devel
BuildRequires:	ftgl-devel
BuildRequires:	gcc >= 5:3.4.0
BuildRequires:	gettext-tools
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	python3-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.385
BuildRequires:	sed >= 4.0
#BuildRequires:	smpeg-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	zlib-devel
Requires(post,postun):	desktop-file-utils
Requires:	OpenGL
Requires:	freetype
Requires:	python-modules
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1

%description
Blender is a free and fully functional 3D modeling, rendering,
animation and game creation package for Unix, Windows and BeOS
systems.

%description -l pl.UTF-8
Blender to darmowy i w pełni funkcjonalny pakiet do tworzenia animacji
3D oraz gier, dostępny dla systemów Unix, Windows i BeOS.

%prep
%setup -q
%patch0 -p1

%build
install -d build
cd build
%cmake \
	-DCMAKE_SKIP_RPATH=ON \
	-DBUILD_SHARED_LIBS=OFF \
	-DWITH_FFTW3:BOOL=ON \
	-DWITH_JACK:BOOL=ON \
	-DWITH_CODEC_SNDFILE:BOOL=ON \
	-DWITH_IMAGE_OPENJPEG:BOOL=ON \
	-DWITH_OPENCOLLADA:BOOL=ON \
	-DWITH_CYCLES:BOOL=ON \
	-DWITH_FFTW3:BOOL=ON \
	-DWITH_MOD_OCEANSIM:BOOL=ON \
	-DOPENCOLLADA=%{_includedir} \
	-DWITH_PYTHON:BOOL=ON \
	-DPYTHON_VERSION:STRING=%{py3_ver} \
	-DWITH_PYTHON_INSTALL:BOOL=OFF \
	-DWITH_CODEC_FFMPEG:BOOL=ON \
	-DWITH_GAMEENGINE:BOOL=ON \
	-DWITH_CXX_GUARDEDALLOC:BOOL=OFF \
	-DWITH_BUILTIN_GLEW=OFF \
	-DWITH_INSTALL_PORTABLE=OFF \
	-DWITH_PYTHON_SAFETY=ON \
	-DWITH_PLAYER=ON \
	-DWITH_MEM_JEMALLOC=ON \
	-DBOOST_ROOT=%{_prefix} \
	-DWITH_INPUT_NDOF=ON \
	-DWITH_SDL:BOOL=ON \
	..

%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_mandir}/man1}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_mandir}/man1/blender.1

#%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files
%defattr(644,root,root,755)
# -f %{name}.lang
%doc doc/license/bf-members.txt doc/guides/*.txt
%attr(755,root,root) %{_bindir}/blender
%attr(755,root,root) %{_bindir}/blender-thumbnailer.py
%attr(755,root,root) %{_bindir}/blenderplayer
%attr(755,root,root) %{_datadir}/%{name}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
%{_iconsdir}/*/*x*/apps/blender.png
%{_iconsdir}/*/scalable/apps/blender.svg
%{_mandir}/man1/*
