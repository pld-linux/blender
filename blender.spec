# TODO:
# - check BRs
#
Summary:	3D modeling, rendering, animation and game creation package
Summary(pl):	Pakiet do tworzenia animacji 3D oraz gier
Name:		blender
Version:	2.28
Release:	0.1
License:	GPL
Group:		X11/Applications/Graphics
Source0:	http://download.blender.org/source/%{name}-%{version}.tar.bz2
# Source0-md5:	4c86e9d28c6ca70b80375fd2c75423bb
Source1:	%{name}.desktop
Source2:	%{name}.png
BuildRequires:	OpenAL-devel
BuildRequires:	OpenGL-devel
BuildRequires:	SDL-devel
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	esound-devel
BuildRequires:	libjpeg-devel
BuildRequires:	libpng-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	libvorbis-devel
BuildRequires:	openssl-devel >= 0.9.7c
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
install -d $RPM_BUILD_ROOT{%{_applnkdir},%{_pixmapsdir}}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -c %{SOURCE1} $RPM_BUILD_ROOT%{_applnkdir}
install -c %{SOURCE2} $RPM_BUILD_ROOT%{_pixmapsdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/*
%{_applnkdir}/%{name}.desktop
%{_pixmapsdir}/%{name}.png
