
Summary:	3D modeling, rendering, animation and game creation package
Summary(pl):	Pakiet do tworzenia animacji 3D oraz robienia gier
Name:		blender
Version:	2.25b.9
Release:	1
License:	GPL
Group:		X11/Applications/Graphics
Vendor:		http://www.linux.ucla.edu/~phaethon/blender/blender-autoconf.html
Source0:	http://www.linux.ucla.edu/~phaethon/blender/blender-creator-ph-%{version}.tar.gz
URL:		http://www.linux.ucla.edu/~phaethon/blender/blender-autoconf.html
#Vendor:		Blender Foundation
#Source0:	ftp://dl.xs4all.nl/pub/mirror/blender/%{name}-source-%{version}.tar.gz
#http://www.linux.ucla.edu/~phaethon/blender/blender-autoconf.html
Requires:	OpenGL
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

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README
%attr(755,root,root) %{_bindir}/blender
%dir %{_libdir}/blender
%attr(755,root,root) %{_libdir}/blender/blender
%{_libdir}/blender/plugins
%{_datadir}/blender
%{_includedir}/blender
%dir %{_examplesdir}/blender
%dir %{_examplesdir}/blender/plugins
%attr(755,root,root) %{_examplesdir}/blender/plugins/bmake
%attr(755,root,root) %{_examplesdir}/blender/plugins/Makefile
%{_examplesdir}/blender/plugins/texture
%{_examplesdir}/blender/plugins/sequence
