# TODO:
# - enable internalization support (BR libftgl)
# - DRACO (requires WITH_PYTHON_INSTALL?)
# - OSL, Cycles
# - Alembic
# - USD
# - OpenImageDenoise
# - OpenSubdiv
# - OptiX >= 7.3.0
# - NanoVDB
# - OpenPGL
#
# Conditional build:
%bcond_without	openvdb	# OpenVDB support

Summary:	3D modeling, rendering, animation and game creation package
Summary(pl.UTF-8):	Pakiet do tworzenia animacji 3D oraz gier
Name:		blender
Version:	4.4.0
Release:	1
License:	GPL v2+
Group:		X11/Applications/Graphics
Source0:	https://download.blender.org/source/%{name}-%{version}.tar.xz
# Source0-md5:	3119090d2744733970ec2345b1f3db94
Patch0:		numpy2.patch
URL:		https://www.blender.org/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenCOLLADA-devel
BuildRequires:	OpenColorIO-devel >= 2.0.0
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenImageIO-devel
BuildRequires:	OpenXR-devel
BuildRequires:	SDL2-devel
BuildRequires:	boost-devel >= 1.48
BuildRequires:	cmake >= 3.10
BuildRequires:	embree-devel >= 3.8.0
BuildRequires:	ffmpeg-devel >= 0.4.9-4.20080930.1
BuildRequires:	fftw3-devel >= 3
BuildRequires:	freealut-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	ftgl-devel
BuildRequires:	gcc >= 5:3.4.0
BuildRequires:	gettext-tools
BuildRequires:	gmp-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	jemalloc-devel
BuildRequires:	libdecor-devel >= 0.1
BuildRequires:	libepoxy-devel
BuildRequires:	libgomp-devel
BuildRequires:	libharu-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libspnav-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libvorbis-devel
BuildRequires:	libwebp-devel
BuildRequires:	libxml2-devel >= 2.0
BuildRequires:	openjpeg2-devel >= 2
BuildRequires:	openssl-devel >= 0.9.7d
%{?with_openvdb:BuildRequires:	openvdb-devel}
BuildRequires:	pcre-devel
BuildRequires:	pkgconfig
BuildRequires:	potrace-devel
BuildRequires:	pugixml-devel
BuildRequires:	pulseaudio-devel
BuildRequires:	python3 >= 1:3.10
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-numpy-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	tbb-devel
# wayland-client, wayland-cursor, wayland-scanner
BuildRequires:	wayland-devel >= 1.12
BuildRequires:	wayland-egl-devel
BuildRequires:	wayland-protocols >= 1.31
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXext-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xorg-lib-libxkbcommon-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
Requires(post,postun):	desktop-file-utils
Requires:	OpenGL
Requires:	python3-modules >= 1:3.10
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# blender needs -march=x86-64-v2, let it pick
%define		filterout_c	-march=x86-64 -mtune=generic
%define		filterout_cxx	-march=x86-64 -mtune=generic

%description
Blender is a free and fully functional 3D modeling, rendering,
animation and game creation package for Unix, Windows and BeOS
systems.

%description -l pl.UTF-8
Blender to darmowy i w pełni funkcjonalny pakiet do tworzenia animacji
3D oraz gier, dostępny dla systemów Unix, Windows i BeOS.

%prep
%setup -q
%patch -P 0 -p1

%build
install -d build
cd build
%cmake \
	-DBOOST_ROOT=%{_prefix} \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DCMAKE_SKIP_RPATH:BOOL=ON \
	-DPYTHON_VERSION:STRING=%{py3_ver} \
	-DWITH_CODEC_FFMPEG:BOOL=ON \
	-DWITH_CODEC_SNDFILE:BOOL=ON \
	-DWITH_CXX_GUARDEDALLOC:BOOL=OFF \
	-DWITH_CYCLES:BOOL=ON \
	-DWITH_FFTW3:BOOL=ON \
	-DWITH_IMAGE_OPENJPEG:BOOL=ON \
	-DWITH_INPUT_NDOF:BOOL=ON \
	-DWITH_INSTALL_PORTABLE:BOOL=OFF \
	-DWITH_JACK:BOOL=ON \
	-DWITH_JACK_DYNLOAD:BOOL=ON \
	-DWITH_MEM_JEMALLOC:BOOL=ON \
	-DWITH_MOD_OCEANSIM:BOOL=ON \
	-DWITH_OPENCOLLADA:BOOL=ON \
	-DWITH_OPENCOLORIO:BOOL=ON \
	%{!?with_openvdb:-DWITH_OPENVDB:BOOL=OFF} \
	-DWITH_PYTHON:BOOL=ON \
	-DWITH_PYTHON_INSTALL:BOOL=OFF \
	-DWITH_PYTHON_SAFETY:BOOL=ON \
	-DWITH_SDL:BOOL=ON \
	-DWITH_SDL_DYNLOAD:BOOL=ON \
	..

%{__make} V=1

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_desktopdir},%{_pixmapsdir},%{_mandir}/man1}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

./doc/manpage/blender.1.py \
	--blender $RPM_BUILD_ROOT%{_bindir}/blender \
	--output $RPM_BUILD_ROOT%{_mandir}/man1/blender.1

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
%attr(755,root,root) %{_bindir}/blender-thumbnailer
%attr(755,root,root) %{_datadir}/%{name}
%{_desktopdir}/blender.desktop
%{_datadir}/metainfo/org.blender.Blender.metainfo.xml
%{_iconsdir}/hicolor/scalable/apps/blender.svg
%{_iconsdir}/hicolor/symbolic/apps/blender-symbolic.svg
%{_mandir}/man1/blender.1*
