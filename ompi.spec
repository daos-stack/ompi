Name:		ompi
Version:	3.0.0rc4
Release:	7%{?dist}

Summary:	OMPI

Group:		Development/Libraries
License:	FOSS
URL:		https://github.com/open-mpi/ompi
Source0:	https://www.github.com/open-mpi/%{name}/archive/v%{version}.tar.gz


BuildRequires: hwloc-devel
BuildRequires: pmix-devel >= 2.1.1
BuildRequires: libevent-devel
BuildRequires: flex
BuildRequires: gcc-c++
%if 0%{?suse_version} > 1310
BuildRequires: gcc-fortran
Obsoletes: openmpi3 < %{version}-%{release}
Obsoletes: openmpi3-libs < %{version}-%{release}
%else
BuildRequires: gcc-gfortran
Obsoletes: openmpi < %{version}-%{release}
Obsoletes: openmpi-libs < %{version}-%{release}
%endif
BuildRequires: pkgconfig

# to be able to generate configure if not present
BuildRequires: autoconf, automake, libtool


%description
OMPI

%package devel
Summary:	OMPI devel package
Requires: %{name}%{?_isa} = %{version}-%{release}

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

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%{_libdir}/*.so.*
%{_libdir}/openmpi
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
* Tue Oct 01 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-7
- Rebuild due to SUSE removing previous libhwloc5 RPM when
  updating to a newer hwloc

* Thu Sep 19 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-6
- devel subpackage needs to require the library subpackage

* Wed Sep 11 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-5
- Obsoletes openmpi-libs for SLES 12.3
- Add BR: gcc-c++, gcc-fortran

* Wed May 01 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-4
- Change source to more stable "archive" URL
- Only include files under include/ in -devel
- Remove all .la files
- Remove perl-Data-Dumper BuildRequires

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
