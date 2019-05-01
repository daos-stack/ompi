Name:		ompi
Version:	3.0.0rc4
Release:	4%{?dist}

Summary:	OMPI

Group:		Development/Libraries
License:	FOSS
URL:		http://ompi-hpc.github.io/documentation/
Source0:        https://www.github.com/open-mpi/%{name}/archive/v%{version}.tar.gz


BuildRequires: hwloc-devel
BuildRequires: pmix-devel >= 2.1.1
BuildRequires: libevent-devel
BuildRequires: perl-Data-Dumper
BuildRequires: flex

# to be able to generate configure if not present
BuildRequires: autoconf, automake, libtool

Obsoletes: openmpi

%description
OMPI

%package devel
Summary:	OMPI devel package

%description devel
OMPI devel

%prep
%setup -q

%build
if [ ! -f configure ]; then
    ./autogen.pl --no-oshmem
    # convert some /usr/lib searches to /usr/lib64
    sed -i -e 's/lib\(\/libpmix\.\*\)/lib64\1/' configure
fi
%configure --with-platform=optimized           \
            --enable-orterun-prefix-by-default \
            --disable-mpi-fortran              \
            --enable-contrib-no-build=vt       \
            --with-libevent=external           \
            --with-pmix=/usr                   \
            --with-hwloc=/usr

make %{?_smp_mflags} V=1

%install
%make_install
find %{?buildroot} -name *.la -print0 | xargs -r0 rm -f

%files
%{_libdir}/*.so.*
%{_libdir}/openmpi/*.so
%{_bindir}/*
%{_datadir}/openmpi/
%{_sysconfdir}/*
%{_mandir}/man1/*
%doc

%files devel
%{_includedir}/*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*
%{_mandir}/man3/*
%{_mandir}/man7/*

%changelog
* Wed May 01 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-4
- Change source to more stable "archive" URL
- Only include files under include/ in -devel
- Remove all .la files

* Mon Mar 18 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-3
- Add a required verison of >= 2.1.1 for pmix-devel to make sure
  to use our build which is newer than EPEL

* Mon Mar 18 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-2
- Obsoletes openmpi
- Don't package libtool .la files
- Include %{_libdir}/openmpi/ in the main package
- Only include the %{_libdir}/pkgconfig/* files in the devel package

* Wed Mar 13 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-1
- initial package
