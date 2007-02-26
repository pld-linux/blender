# TODO:
# - enable internalization support (BR libftgl)
# - enable OpenAL support
# - libsolid/libqhull/libode BR ?
# - package python scripts
Summary:	3D modeling, rendering, animation and game creation package
Summary(pl.UTF-8):	Pakiet do tworzenia animacji 3D oraz gier
Name:		blender
Version:	2.43
Release:	0.1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://download.blender.org/source/%{name}-%{version}.tar.gz
# Source0-md5:	7629c31bc45e286bdf3b2c555e6446a2
Source1:	%{name}.desktop
Source2:	%{name}.png
Source4:	%{name}-wrapper
Source5:	%{name}.manpage
Patch0:		%{name}-po_and_locale_names.patch
Patch1:		%{name}-noxml-yafray.patch
Patch2:		%{name}-python-fix.patch
URL:		http://www.blender.org/
BuildRequires:	OpenEXR-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	freealut-devel
BuildRequires:	freetype-devel
BuildRequires:	ftgl-devel
BuildRequires:	gettext-devel
#BuildRequires:	esound-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtiff-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	scons
BuildRequires:	sed >= 4.0
#BuildRequires:	smpeg-devel
BuildRequires:	zlib-devel
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
%patch2 -p1
mv -f po/pt_{br,BR}.po

rm -f missing
rm -f user-config.py

RPMCFLAGS="\"`echo %{rpmcflags}|sed 's/ /\",\"/g'`\""
RPMLDFLAGS="\"`echo %{rpmldflags}|sed 's/ /\",\"/g'`\""

cat > user-config.py <<END
CCFLAGS           = [$RPMCFLAGS]
CXXFLAGS          = [$RPMCFLAGS]
LDFLAGS           = [$RPMLDFLAGS]
TARGET_CC         = '%{__cc}'
TARGET_CXX        = '%{__cxx}'

BF_PYTHON_VERSION = '%{py_ver}'

LCGDIR            = 'lib/linux2'
BF_BUILDDIR       = 'build/linux2'
BF_INSTALLDIR     = 'install/linux2'
END

%build
scons
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
cp -a bin/.blender/locale $RPM_BUILD_ROOT%{_datadir}/blender
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install %{SOURCE5} $RPM_BUILD_ROOT%{_mandir}/man1/blender.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README doc/bf-members.txt doc/python-dev-guide.txt doc/oldbugs.txt doc/interface_API.txt
%doc release/text/{blender.html,release*.txt}
%attr(755,root,root) %{_bindir}/*
%attr(755,root,root) %{_datadir}/%{name}
%attr(755,root,root) %{_libdir}/%{name}
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
%{_mandir}/man1/*
