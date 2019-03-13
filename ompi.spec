Name:		ompi
Version:	3.0.0rc4
Release:	1%{?dist}

Summary:	OMPI

Group:		Development/Libraries
License:	FOSS
URL:		http://ompi-hpc.github.io/documentation/
Source0:        https://www.github.com/open-mpi/%{name}/releases/download/v%{version}/%{name}-%{version}.tar.gz

BuildRequires: hwloc-devel
BuildRequires: pmix-devel
BuildRequires: libevent-devel
BuildRequires: perl-Data-Dumper
BuildRequires: flex

# to be able to generate configure if not present
BuildRequires: autoconf, automake, libtool

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


%files
%{_libdir}/*.so.*
%{_bindir}/
%{_datadir}/openmpi/
%{_sysconfdir}/*
%{_mandir}/man1/*
%doc

%files devel
%{_includedir}
%{_libdir}/*.so
%{_libdir}/*.la
%{_libdir}/openmpi/*.so
%{_libdir}/openmpi/*.la
%{_libdir}/pkgconfig
%{_mandir}/man3/*
%{_mandir}/man7/*

%changelog
* Wed Mar 13 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-1
- initial package
