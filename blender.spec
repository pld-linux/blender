
%include /usr/lib/rpm/macros.python

Summary:	3D modeling, rendering, animation and game creation package
Summary(pl):	Pakiet do tworzenia animacji 3D oraz robienia gier
Name:		blender
Version:	2.25b.9
Release:	0.1
License:	GPL
Group:		X11/Applications/Graphics
Vendor:		http://www.linux.ucla.edu/~phaethon/blender/blender-autoconf.html
Source0:	http://www.linux.ucla.edu/~phaethon/blender/blender-creator-ph-%{version}.tar.gz
URL:		http://www.linux.ucla.edu/~phaethon/blender/blender-autoconf.html
#!#Vendor:		Blender Foundation
#!#Source0:	ftp://dl.xs4all.nl/pub/mirror/blender/%{name}-source-%{version}.tar.gz
#!#http://www.linux.ucla.edu/~phaethon/blender/blender-autoconf.html
Patch0:		%{name}-python.patch
Requires:	OpenGL
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	openssl-devel
BuildRequires:	python-devel
BuildRequires:	smpeg-devel
BuildRequires:	zlib-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_prefix		/usr/X11R6

%description
Blender is a free and fully functional 3D modeling, rendering,
animation and game creation package for Unix, Windows and BeOS
systems.

%description -l pl
Blender to darmowy i w pe�ni funkcjonalny pakiet do tworzenia animacji
3D oraz robienia gier, dost�pny dla system�w Unix, Windows i BeOS.

%prep
%setup -q -n %{name}-creator-ph-%{version}
%patch0 -p1

%build
CPPFLAGS="-I/usr/X11R6/include"
LDFLAGS="-L/usr/X11R6/lib"
export CPPFLAGS LDFLAGS
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT
echo blender-creator-ph > $RPM_BUILD_ROOT%{py_sitedir}/blender.pth

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%dir %{py_sitedir}/blender-creator-ph
%attr(755,root,root) %{py_sitedir}/blender-creator-ph/*.so
%{py_sitedir}/blender.pth
