
%include /usr/lib/rpm/macros.python

Summary:	3D modeling, rendering, animation and game creation package
Summary(pl):	Pakiet do tworzenia animacji 3D oraz robienia gier
Name:		blender
Version:	2.27
Release:	0.1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://download.blender.org/source/%{name}-%{version}.tar.bz2
# Source0-md5:	2b34e7ad67d02771a3fae0411c6fe845
Patch0:		%{name}-python.patch
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libtool
BuildRequires:	openssl-devel >= 0.9.7
BuildRequires:	python-devel
BuildRequires:	smpeg-devel
BuildRequires:	zlib-devel
Requires:	OpenGL
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1

%description
Blender is a free and fully functional 3D modeling, rendering,
animation and game creation package for Unix, Windows and BeOS
systems.

%description -l pl
Blender to darmowy i w pe³ni funkcjonalny pakiet do tworzenia animacji
3D oraz robienia gier, dostêpny dla systemów Unix, Windows i BeOS.

%prep
%setup -q
#%patch0 -p1

%build
CPPFLAGS="-I/usr/X11R6/include"
LDFLAGS="-L/usr/X11R6/lib"
export CPPFLAGS LDFLAGS
#%{__libtoolize}
#%{__aclocal}
#%{__autoconf}
#%{__automake}
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT
#echo blender-creator-ph > $RPM_BUILD_ROOT%{py_sitedir}/blender.pth

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
#%dir %{py_sitedir}/blender-creator-ph
#%attr(755,root,root) %{py_sitedir}/blender-creator-ph/*.so
#%{py_sitedir}/blender.pth
