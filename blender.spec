Summary:	3D modeling, rendering, animation and game creation package
Summary(pl):	Pakiet do tworzenia animacji 3D oraz gier
Name:		blender
Version:	2.30
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://download.blender.org/source/%{name}-%{version}.tar.bz2
# Source0-md5:	6e413db3bdd6208ad47c35b66ce1fe58
Source1:	%{name}.desktop
Source2:	%{name}.png
URL:		http://www.blender.org/
#BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	autoconf
BuildRequires:	automake
#BuildRequires:	esound-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	openssl-devel >= 0.9.7c
BuildRequires:	python-devel
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

%build
rm -f missing
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_datadir},%{_desktopdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -c %{SOURCE1} $RPM_BUILD_ROOT%{_desktopdir}
install -c %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}
cp -a bin/.blender/locale $RPM_BUILD_ROOT%{_datadir}

%find_lang %{name} --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README release*.txt
%attr(755,root,root) %{_bindir}/*
%{_desktopdir}/*.desktop
%{_pixmapsdir}/*.png
