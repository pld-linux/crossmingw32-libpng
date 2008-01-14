%define		realname	libpng
Summary:	PNG library - Mingw32 cross version
Summary(pl.UTF-8):	Biblioteka PNG - wersja skrośna dla Mingw32
Name:		crossmingw32-%{realname}
Version:	1.2.24
Release:	1
License:	distributable
Group:		Development/Libraries
Source0:	http://dl.sourceforge.net/libpng/%{realname}-%{version}.tar.bz2
# Source0-md5:	1e676c5cc7dfa4ef78affe8fb8f1011d
Patch0:		%{realname}-pngminus.patch
Patch1:		%{realname}-opt.patch
Patch2:		%{realname}-revert.patch
Patch3:		%{realname}-norpath.patch
Patch4:		%{name}-shared.patch
URL:		http://www.libpng.org/pub/png/libpng.html
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-zlib
Requires:	crossmingw32-zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target			i386-mingw32
%define		target_platform		i386-pc-mingw32

%define		_sysprefix		/usr
%define		_prefix			%{_sysprefix}/%{target}
%define		_libdir			%{_prefix}/lib
%define		_pkgconfigdir		%{_prefix}/lib/pkgconfig
%define		_dlldir			/usr/share/wine/windows/system
%define		__cc			%{target}-gcc
%define		__cxx			%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

%description
The PNG library is a collection of routines used to create and
manipulate PNG format graphics files. The PNG format was designed as a
replacement for GIF, with many improvements and extensions.

This package contains the cross version for Win32.

%description -l pl.UTF-8
Biblioteki PNG są kolekcją form używanych do tworzenia i manipulowania
plikami w formacie graficznym PNG. Format ten został stworzony jako
zamiennik dla formatu GIF, z wieloma rozszerzeniami i nowościami.

Ten pakiet zawiera wersję skrośną dla Win32.

%package static
Summary:	Static libpng library (cross mingw32 version)
Summary(pl.UTF-8):	Statyczna biblioteka libpng (wersja skrośna mingw32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description static
Static libpng library (cross mingw32 version).

%description static -l pl.UTF-8
Statyczna biblioteka libpng (wersja skrośna mingw32).

%package dll
Summary:	libpng - DLL library for Windows
Summary(pl.UTF-8):	libpng - biblioteka DLL dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-zlib-dll
Requires:	wine

%description dll
libpng - DLL library for Windows.

%description dll -l pl.UTF-8
libpng - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

%build
%configure \
	--target=%{target} \
	--host=%{target} \
	--with-pkgconfigdir=%{_pkgconfigdir}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_dlldir}
mv -f $RPM_BUILD_ROOT%{_prefix}/bin/*.dll $RPM_BUILD_ROOT%{_dlldir}

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

rm -rf $RPM_BUILD_ROOT%{_datadir}/man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/libpng.dll.a
%{_libdir}/libpng12.dll.a
%{_libdir}/libpng.la
%{_libdir}/libpng12.la
%dir %{_includedir}/libpng12
%{_includedir}/libpng12/*
%{_pkgconfigdir}/*.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpng.a
%{_libdir}/libpng12.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libpng-*.dll
%{_dlldir}/libpng12-*.dll
