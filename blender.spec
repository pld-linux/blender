# TODO:
# - enable internalization support (BR libftgl)
# - enable OpenAL support
# - libsolid/libqhull/libode BR ?
# - package python scripts
Summary:	3D modeling, rendering, animation and game creation package
Summary(pl):	Pakiet do tworzenia animacji 3D oraz gier
Name:		blender
Version:	2.37a
# 2.37a is not alpha. Is the latest, STABLE version of blender.
Release:	2
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://download.blender.org/source/%{name}-%{version}.tar.gz
# Source0-md5:	dd0002c09ecd68b3cb3e3d8f4ce31e83
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:	%{name}-config.opts
Source4:	%{name}-wrapper
Source5:	%{name}.manpage
Patch0:		%{name}-po_and_locale_names.patch
Patch1:		%{name}-noxml-yafray.patch
URL:		http://www.blender.org/
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	ftgl-devel
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	esound-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	freetype-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	python-devel >= 1:2.3
BuildRequires:	scons
BuildRequires:	sed >= 4.0
#BuildRequires:	smpeg-devel
BuildRequires:	zlib-devel
Requires:	OpenGL
Requires:	python-modules
Requires:       freetype
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1

%description
Blender is a free and fully functional 3D modeling, rendering,
animation and game creation package for Unix, Windows and BeOS
systems.

%description -l pl
Blender to darmowy i w pe³ni funkcjonalny pakiet do tworzenia animacji
3D oraz gier, dostêpny dla systemów Unix, Windows i BeOS.

%prep
%setup -q -n %{name}
%patch0 -p1
%patch1 -p1
mv -f po/pt_{br,BR}.po
install %{SOURCE3} config.opts

%build
rm -f missing

RPMCFLAGS="\"`echo %{rpmcflags}|sed 's/ /\",\"/g'`\""
RPMLDFLAGS="\"`echo %{rpmldflags}|sed 's/ /\",\"/g'`\""

sed -i -e "s|^CCFLAGS =.*|CCFLAGS = [$RPMCFLAGS]|" \
	-e "s|^CXXFLAGS =.*|CXXFLAGS = [$RPMCFLAGS]|" \
	-e "s|^LDFLAGS =.*|LDFLAGS = [$RPMLDFLAGS]|" \
	config.opts
sed -i -e "s|TARGET_CC =.*|TARGET_CC = '%{__cc}'|" \
	-e "s|TARGET_CXX =.*|TARGET_CXX = '%{__cxx}'|" \
	config.opts
sed -i 's/python2\.3/python%{py_ver}/' config.opts

scons
%{__make} -C po OCGDIR=..

install -d release/plugins/include
install source/blender/blenpluginapi/*.h release/plugins/include
chmod +x release/plugins/bmake
%{__make} -C release/plugins/

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_desktopdir},%{_pixmapsdir},%{_bindir}}

install blender $RPM_BUILD_ROOT%{_bindir}/blender-bin
install %{SOURCE4} $RPM_BUILD_ROOT%{_bindir}/blender
install blenderplayer $RPM_BUILD_ROOT%{_bindir}
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
