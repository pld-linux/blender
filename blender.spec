# TODO:
# - enable internalization support (BR libftgl)
# - libsolid/libqhull/libode BR ?
Summary:	3D modeling, rendering, animation and game creation package
Summary(pl.UTF-8):	Pakiet do tworzenia animacji 3D oraz gier
Name:		blender
Version:	3.1.0
Release:	3
License:	GPL
Group:		X11/Applications/Graphics
Source0:	https://download.blender.org/source/%{name}-%{version}.tar.xz
# Source0-md5:	483e16f010cc8c2363ba05b716fde3d0
Patch0:		%{name}-2.76-droid.patch
Patch1:		format-security.patch
Patch2:		boost1.81.patch
URL:		https://www.blender.org/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenColorIO-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-devel
BuildRequires:	OpenGL-GLU-devel
BuildRequires:	OpenImageIO-devel
BuildRequires:	SDL2-devel
BuildRequires:	boost-devel
BuildRequires:	cmake
BuildRequires:	embree-devel
BuildRequires:	ffmpeg-devel >= 0.4.9-4.20080930.1
BuildRequires:	fftw3-devel
BuildRequires:	freealut-devel
BuildRequires:	freetype-devel
BuildRequires:	ftgl-devel
BuildRequires:	gcc >= 5:3.4.0
BuildRequires:	gettext-tools
BuildRequires:	glew-devel
BuildRequires:	jack-audio-connection-kit-devel
BuildRequires:	jemalloc-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libsndfile-devel
BuildRequires:	libspnav-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	openjpeg2-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	pugixml-devel
BuildRequires:	python3 >= 1:3.10
BuildRequires:	python3-devel >= 1:3.10
BuildRequires:	python3-numpy-devel
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xorg-lib-libXi-devel
BuildRequires:	xz
BuildRequires:	zlib-devel
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
%patch2 -p1

%{__sed} -E -i -e '1s,#!\s*/usr/bin/env\s+python(\s|$),#!%{__python3}\1,' -e '1s,#!\s*/usr/bin/env\s+python3(\s|$),#!%{__python3}\1,' \
      release/scripts/addons/io_curve_svg/svg_util_test.py \
      release/scripts/addons/io_scene_fbx/fbx2json.py \
      release/scripts/addons/io_scene_fbx/json2fbx.py \
      release/scripts/addons/sun_position/geo.py \
      release/scripts/modules/bl_i18n_utils/merge_po.py \
      release/scripts/modules/bl_i18n_utils/utils_rtl.py \
      release/scripts/modules/blend_render_info.py

%build
install -d build
cd build
%cmake \
	-DCMAKE_SKIP_RPATH:BOOL=ON \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DWITH_FFTW3:BOOL=ON \
	-DWITH_JACK:BOOL=ON \
	-DWITH_JACK_DYNLOAD:BOOL=ON \
	-DWITH_CODEC_SNDFILE:BOOL=ON \
	-DWITH_IMAGE_OPENJPEG:BOOL=ON \
	-DWITH_OPENCOLLADA:BOOL=ON \
	-DWITH_OPENCOLORIO:BOOL=ON \
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
	-DWITH_INSTALL_PORTABLE:BOOL=OFF \
	-DWITH_PYTHON_SAFETY:BOOL=ON \
	-DWITH_PLAYER:BOOL=ON \
	-DWITH_MEM_JEMALLOC:BOOL=ON \
	-DWITH_SYSTEM_GLEW:BOOL=ON \
	-DBOOST_ROOT=%{_prefix} \
	-DWITH_INPUT_NDOF:BOOL=ON \
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
%{_desktopdir}/*.desktop
%{_iconsdir}/hicolor/scalable/apps/blender.svg
%{_iconsdir}/hicolor/symbolic/apps/blender-symbolic.svg
%{_mandir}/man1/*
