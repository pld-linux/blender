# TODO:
# - enable internalization support (BR libftgl)
# - libsolid/libqhull/libode BR ?
Summary:	3D modeling, rendering, animation and game creation package
Summary(pl.UTF-8):	Pakiet do tworzenia animacji 3D oraz gier
Name:		blender
Version:	2.48a
Release:	4
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://download.blender.org/source/%{name}-%{version}.tar.gz
# Source0-md5:	055d68d244458e9e429e4e492fc9b4ad
Source1:	%{name}.desktop
Source2:	%{name}.png
Source4:	%{name}-wrapper
Source5:	%{name}.manpage
Patch0:		%{name}-po_and_locale_names.patch
Patch1:		%{name}-noxml-yafray.patch
Patch2:		%{name}-ffmpeg.patch
URL:		http://www.blender.org/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
#BuildRequires:	esound-devel
BuildRequires:	ffmpeg-devel >= 0.4.9-4.20080930.1
BuildRequires:	freealut-devel
BuildRequires:	freetype-devel
BuildRequires:	ftgl-devel
BuildRequires:	gcc >= 5:3.4.0
BuildRequires:	gettext-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	rpmbuild(macros) >= 1.385
BuildRequires:	scons
BuildRequires:	sed >= 4.0
#BuildRequires:	smpeg-devel
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
%patch1 -p1
%patch2 -p0

rm -f missing
rm -f user-config.py
rm -rf bin/.blender/locale

RPMCFLAGS="\"`echo %{rpmcflags}|sed 's/ /\",\"/g'`\""
RPMLDFLAGS="\"`echo %{rpmldflags}|sed 's/ /\",\"/g'`\""

cat > user-config.py <<END
CCFLAGS           = [$RPMCFLAGS, "-funsigned-char", "-fPIC"]
CXXFLAGS          = [$RPMCFLAGS, "-funsigned-char", "-fPIC"]
LDFLAGS           = [$RPMLDFLAGS]
TARGET_CC         = '%{__cc}'
TARGET_CXX        = '%{__cxx}'

BF_PYTHON_VERSION = '%{py_ver}'

BF_FFMPEG         = '%{_prefix}'
BF_FFMPEG_INC     = '%{_includedir}/ffmpeg'
BF_FFMPEG_LIBPATH = '%{_libdir}'
BF_FFMPEG_LIB     = 'avformat avcodec swscale avutil'

LCGDIR            = 'lib/linux2'
BF_BUILDDIR       = 'build/linux2'
BF_INSTALLDIR     = 'install/linux2'
END

%build
%scons BF_OPENGL_LIBPATH=%{_x_libraries}
%{__make} -C po OCGDIR=..

install -d release/plugins/include
install source/blender/blenpluginapi/*.h release/plugins/include
chmod +x release/plugins/bmake
%{__make} -C release/plugins/

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_desktopdir},%{_pixmapsdir},%{_bindir}} \
	$RPM_BUILD_ROOT%{_datadir}/blender/bpydata

install ./install/linux2/blender $RPM_BUILD_ROOT%{_bindir}/blender-bin
install %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/blender
#install blenderplayer $RPM_BUILD_ROOT%{_bindir}
install %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
install -d $RPM_BUILD_ROOT%{_libdir}/blender/plugins/sequence
install -d $RPM_BUILD_ROOT%{_libdir}/blender/plugins/texture
install ./release/plugins/sequence/*.so $RPM_BUILD_ROOT%{_libdir}/blender/plugins/sequence
install ./release/plugins/texture/*.so $RPM_BUILD_ROOT%{_libdir}/blender/plugins/texture
install -d $RPM_BUILD_ROOT%{_datadir}/blender
cp -aR ./release/scripts $RPM_BUILD_ROOT%{_datadir}/blender
install ./release/VERSION $RPM_BUILD_ROOT%{_datadir}/blender
install ./bin/.blender/.Blanguages $RPM_BUILD_ROOT%{_datadir}/blender
install ./bin/.blender/.bfont.ttf $RPM_BUILD_ROOT%{_datadir}/blender
cp -a bin/.blender/locale $RPM_BUILD_ROOT%{_datadir}
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man1/blender.1

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_desktop_database_post

%postun
%update_desktop_database_postun

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README doc/bf-members.txt doc/python-dev-guide.txt doc/oldbugs.txt doc/interface_API.txt
%doc release/text/{blender.html,release*.txt}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_datadir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
%{_mandir}/man1/*
