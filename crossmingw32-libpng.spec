%define		realname	libpng
Summary:	PNG library - MinGW32 cross version
Summary(pl.UTF-8):	Biblioteka PNG - wersja skrośna dla MinGW32
Name:		crossmingw32-%{realname}
Version:	1.4.5
Release:	1
License:	distributable
Group:		Development/Libraries
Source0:	http://downloads.sourceforge.net/libpng/%{realname}-%{version}.tar.xz
# Source0-md5:	37d420c7d8294aac438c150bb4335901
Patch0:		%{realname}-pngminus.patch
# http://littlesvr.ca/apng/diff/%{name}-%{version}-apng.patch | dos2unix
Patch1:		%{realname}-apng.patch
URL:		http://www.libpng.org/pub/png/libpng.html
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-zlib
BuildRequires:	sed >= 4.0
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz >= 1:4.999.7
Requires:	crossmingw32-zlib
Provides:	crossmingw32-libpng(APNG) = 0.10
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

%ifnarch %{ix86}
# arch-specific flags (like alpha's -mieee) are not valid for i386 gcc
%define		optflags	-O2
%endif
# -z options are invalid for mingw linker
%define		filterout_ld	-Wl,-z,.*
%define		filterout_c	-gdwarf-3

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
Summary:	Static libpng library (cross MinGW32 version)
Summary(pl.UTF-8):	Statyczna biblioteka libpng (wersja skrośna MinGW32)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Provides:	crossmingw32-libpng-static(APNG) = 0.10

%description static
Static libpng library (cross MinGW32 version).

%description static -l pl.UTF-8
Statyczna biblioteka libpng (wersja skrośna MinGW32).

%package dll
Summary:	libpng - DLL library for Windows
Summary(pl.UTF-8):	libpng - biblioteka DLL dla Windows
Group:		Applications/Emulators
Requires:	crossmingw32-zlib-dll
Requires:	wine
Provides:	crossmingw32-libpng-dll(APNG) = 0.10

%description dll
libpng - DLL library for Windows.

%description dll -l pl.UTF-8
libpng - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p0

# avoid version script
sed -i -e 's/^GLD=.*/GLD=/' configure

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

ln -sf libpng14.dll.a $RPM_BUILD_ROOT%{_libdir}/libpng.dll.a

%if 0%{!?debug:1}
%{target}-strip --strip-unneeded -R.comment -R.note $RPM_BUILD_ROOT%{_dlldir}/*.dll
%{target}-strip -g -R.comment -R.note $RPM_BUILD_ROOT%{_libdir}/*.a
%endif

rm -rf $RPM_BUILD_ROOT%{_datadir}/man

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{_libdir}/libpng14.dll.a
%{_libdir}/libpng.dll.a
%{_libdir}/libpng14.la
%{_libdir}/libpng.la
%{_includedir}/libpng14
%{_includedir}/png*.h
%{_pkgconfigdir}/libpng14.pc
%{_pkgconfigdir}/libpng.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libpng14.a
%{_libdir}/libpng.a

%files dll
%defattr(644,root,root,755)
%{_dlldir}/libpng14-*.dll
