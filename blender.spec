
# chyba nie mo¿emy tego udostêpniaæ na naszym FTP
# przynajmniej ja tak rozumiem fragment copyright.txt:
#
# "Distributing the Software 'bundled' in with ANY product is
#  considered to be a 'commercial purpose'."


%ifarch %{ix86}
%define		arch_name blender%{version}-linux-glibc2.1.2-i386
%endif
%ifarch %{alpha}
%define		arch_name blender%{version}-linux-glibc2.1.3-alpha
%endif

Summary:	3D modeling, rendering, animation and game creation package
Summary(pl):	Pakiet do tworzenia animacji 3D oraz robienia gier
Name:		blender
Version:	2.20
Release:	1
License:	Free for use
Group:		Applications/Graphics
Vendor:		NaN Technologies B.V.
Source0:	ftp://ftp.blender.nl/pub/%{arch_name}.tar.gz
Source1:	%{name}.defaults
Source2:	%{name}.sh
Patch0:		%{name}-bmake.patch
URL:		http://www.blender.nl
Requires:	OpenGL
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define 	_noautoreqdep	libGL.so.1 libGLU.so.1
%define		_prefix		/usr/X11R6

%description
Blender is a free and fully functional 3D modeling, rendering,
animation and game creation package for Unix, Windows and BeOS
systems. Blender is distributed without sources, it is exclusively
developed and maintained by the Dutch company NaN Technologies B.V.

%description -l pl
Blender to darmowy i w pe³ni funkcjonalny pakiet do tworzenia animacji
3D oraz robienia gier, dostêpny dla systemów Unix, Windows i BeOS.
Blender jest rozpowszechniany bez ¼róde³. Jest rozwijany przez
holendersk± firmê NaN Technologies B.V.

%prep
%setup -qn %{arch_name}
%patch0 -p1

%build
cd plugins
%{__make} clean
%{__make} OPTFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/blender/plugins/{sequence,texture}}
install -d $RPM_BUILD_ROOT{%{_datadir}/blender/{textures,sounds},%{_includedir}/blender}
install -d $RPM_BUILD_ROOT%{_examplesdir}/blender/plugins/{sequence,texture}

install %{SOURCE2} $RPM_BUILD_ROOT%{_bindir}/blender

install blender $RPM_BUILD_ROOT%{_libdir}/blender
install plugins/sequence/*.so $RPM_BUILD_ROOT%{_libdir}/blender/plugins/sequence
install plugins/texture/*.so $RPM_BUILD_ROOT%{_libdir}/blender/plugins/texture

install %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/blender/defaults

install plugins/include/* $RPM_BUILD_ROOT%{_includedir}/blender

install plugins/{Makefile,bmake} $RPM_BUILD_ROOT%{_examplesdir}/blender/plugins
install plugins/sequence/{Makefile,*.c} $RPM_BUILD_ROOT%{_examplesdir}/blender/plugins/sequence
install plugins/texture/{Makefile,*.c} $RPM_BUILD_ROOT%{_examplesdir}/blender/plugins/texture

gzip -9nf README copyright.txt

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc *.gz
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
