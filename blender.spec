# TODO:
# - enable internalization support (BR libftgl)
# - libsolid/libqhull/libode BR ?
# - DRACO (requires WITH_PYTHON_INSTALL?)
# - OSL, Cycles
# - Alembic
# - USD
# - OpenImageDenoise
# - OpenSubdiv
# - XR_OpenXR_SDK
# - OptiX >= 7.3.0
#
# Conditional build:
%bcond_with	openvdb	# OpenVDB support (3.1.x is not ready for openvdb 10)

Summary:	3D modeling, rendering, animation and game creation package
Summary(pl.UTF-8):	Pakiet do tworzenia animacji 3D oraz gier
Name:		blender
Version:	3.3.10
Release:	1
License:	GPL v2+
Group:		X11/Applications/Graphics
Source0:	https://download.blender.org/source/%{name}-%{version}.tar.xz
# Source0-md5:	a190dbfc5dfd490d737ee64ba68ce79c
Patch0:		%{name}-2.76-droid.patch
Patch1:		format-security.patch
Patch3:		gcc13.patch
URL:		https://www.blender.org/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenCOLLADA-devel
BuildRequires:	OpenColorIO-devel >= 2.0.0
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenImageIO-devel
BuildRequires:	OpenXR-devel
BuildRequires:	SDL2-devel
BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.10
BuildRequires:	embree-devel >= 3.8.0
BuildRequires:	ffmpeg-devel >= 0.4.9-4.20080930.1
BuildRequires:	fftw3-devel >= 3
BuildRequires:	freealut-devel
BuildRequires:	freetype-devel >= 2
BuildRequires:	ftgl-devel
BuildRequires:	gcc >= 5:3.4.0
BuildRequires:	gettext-tools
BuildRequires:	glew-devel
BuildRequires:	gmp-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	jemalloc-devel
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
BuildRequires:	openjpeg2-devel
%{?with_openvdb:BuildRequires:	openvdb-devel}
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pcre-devel
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
BuildRequires:	xorg-lib-libX11-devel
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
BuildRequires:	zstd-devel
Requires(post,postun):	desktop-file-utils
Requires:	OpenGL
Requires:	freetype
Requires:	python3-modules >= 1:3.10
ExclusiveArch:	%{x8664}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_noautoreqdep	libGL.so.1 libGLU.so.1

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
%patch1 -p1
%patch3 -p1

# not executable
%{__sed} -i -e '/^#!\/usr\/bin\/env python/d' release/scripts/addons/sun_position/geo.py

# /usr/bin/env python3
%{__sed} -i -e '1s,/usr/bin/env python3,%{__python3},' \
	release/scripts/addons/io_curve_svg/svg_util_test.py \
	release/scripts/addons/io_scene_fbx/fbx2json.py \
	release/scripts/addons/io_scene_fbx/json2fbx.py \
	release/scripts/modules/bl_i18n_utils/merge_po.py \
	release/scripts/modules/bl_i18n_utils/utils_rtl.py \
	release/scripts/modules/blend_render_info.py

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
	-DWITH_SYSTEM_GLEW:BOOL=ON \
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
%{_iconsdir}/hicolor/scalable/apps/blender.svg
%{_iconsdir}/hicolor/symbolic/apps/blender-symbolic.svg
%{_mandir}/man1/blender.1*
