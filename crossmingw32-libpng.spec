%define		realname	libpng
Summary:	PNG library - Mingw32 cross version
Summary(pl):	Biblioteka PNG - wersja skro¶na dla Mingw32
Name:		crossmingw32-%{realname}
Version:	1.2.7
Release:	2
License:	distributable
Group:		Libraries
Source0:	http://dl.sourceforge.net/libpng/%{realname}-%{version}.tar.bz2
# Source0-md5:	21030102f99f81c37276403e5956d198
Patch0:		%{realname}-pngminus.patch
Patch1:		%{realname}-badchunks.patch
Patch2:		%{realname}-opt.patch
Patch3:		%{realname}-revert.patch
Patch4:		%{realname}-norpath.patch
Patch5:		%{realname}-libdirfix.patch
Patch6:		%{name}-shared.patch
URL:		http://www.libpng.org/pub/png/libpng.html
BuildRequires:	crossmingw32-gcc
BuildRequires:	crossmingw32-w32api
BuildRequires:	crossmingw32-zlib
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		no_install_post_strip	1

%define		target		i386-mingw32
%define		target_platform	i386-pc-mingw32
%define		arch		%{_prefix}/%{target}
%define		gccarch		%{_prefix}/lib/gcc-lib/%{target}
%define		gcclib		%{_prefix}/lib/gcc-lib/%{target}/%{version}

%define		__cc		%{target}-gcc
%define		__cxx		%{target}-g++

%ifarch alpha sparc sparc64 sparcv9
%define		optflags	-O2
%endif

%description
The PNG library is a collection of routines used to create and
manipulate PNG format graphics files. The PNG format was designed as a
replacement for GIF, with many improvements and extensions.

%description -l pl
Biblioteki PNG s± kolekcj± form u¿ywanych do tworzenia i manipulowania
plikami w formacie graficznym PNG. Format ten zosta³ stworzony jako
zamiennik dla formatu GIF, z wieloma rozszerzeniami i nowo¶ciami.

%package dll
Summary:	libpng - DLL library for Windows
Summary(pl):	libpng - biblioteka DLL dla Windows
Group:		Applications/Emulators

%description dll
libpng - DLL library for Windows.

%description dll -l pl
libpng - biblioteka DLL dla Windows.

%prep
%setup -q -n %{realname}-%{version}
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

%ifarch %{ix86}
ln -sf scripts/makefile.gcmmx ./Makefile
%else
ln -sf scripts/makefile.linux ./Makefile
%endif

%patch6 -p1

%build
%{__make} \
	prefix=%{_arch} \
	LIBPATH=%{_arch}/lib \
	CC="%{target}-gcc" \
	RANLIB="%{target}-ranlib"
	OPT_FLAGS="%{rpmcflags}"

%if 0%{!?debug:1}
%{target}-strip -R.comment -R.note *.dll
%{target}-strip -g -R.comment -R.note *.a
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{arch}/{include,lib}
install -d $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

install *.a $RPM_BUILD_ROOT%{arch}/lib
install png.h pngconf.h $RPM_BUILD_ROOT%{arch}/include
install *.dll $RPM_BUILD_ROOT%{_datadir}/wine/windows/system

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%{arch}/include/*
%{arch}/lib/*

%files dll
%defattr(644,root,root,755)
%{_datadir}/wine/windows/system
