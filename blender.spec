# TODO:
# - enable internalization support (BR libftgl)
# - enable OpenAL support
# - libsolid/libqhull/libode BR ?
# - package python scripts
Summary:	3D modeling, rendering, animation and game creation package
Summary(pl):	Pakiet do tworzenia animacji 3D oraz gier
Name:		blender
Version:	2.35
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://download.blender.org/source/%{name}-%{version}.tar.bz2
# Source0-md5:	d451bb3047a9c2fe785c0b91f9769717
Source1:	%{name}.desktop
Source2:	%{name}.png
Source3:	%{name}-config.opts
Patch0:		%{name}-po_and_locale_names.patch
URL:		http://www.blender.org/
#BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
#BuildRequires:	autoconf
#BuildRequires:	automake
#BuildRequires:	esound-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	openssl-devel >= 0.9.7d
BuildRequires:	python-devel
BuildRequires:	scons
#BuildRequires:	smpeg-devel
BuildRequires:	zlib-devel
Requires:	OpenGL
Requires:	python-modules
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
%setup -q
%patch0 -p1

mv -f po/pt_{br,BR}.po
rm -rf bin/.blender/locale
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
# TODO fix PYTHON_* vars in config.opts

scons
%{__make} -C po OCGDIR=..

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_desktopdir},%{_pixmapsdir},%{_bindir}}

install -m755 blender $RPM_BUILD_ROOT%{_bindir}
install -m755 blenderplayer $RPM_BUILD_ROOT%{_bindir}
install -c %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install -c %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
cp -a bin/.blender/locale $RPM_BUILD_ROOT%{_datadir}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README doc/bf-members.txt doc/python-dev-guide.txt doc/oldbugs.txt doc/interface_API.txt 
%doc release/text/{blender.html,release*.txt}
%attr(755,root,root) %{_bindir}/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
