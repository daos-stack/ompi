%global macrosdir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

%global variant openmpi3
%global libname %{variant}
%global namearch %{variant}-%{_arch}

Name:    ompi
Version: 3.0.0rc4
Release: 9%{?dist}

Summary: OMPI

Group:	 Development/Libraries
License: FOSS
URL:	 https://github.com/open-mpi/ompi
Source0: https://www.github.com/open-mpi/%{name}/archive/v%{version}.tar.gz
Source301: openmpi3.module.in
Source302: macros.openmpi3


BuildRequires: hwloc-devel < 2.0.0
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
BuildRequires: libpsm2-devel >= 11.2.78

# to be able to generate configure if not present
BuildRequires: autoconf, automake, libtool


%description
OMPI

%package devel
Summary:	OMPI devel package
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: libpsm2-devel >= 11.2.78

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
./configure --build=x86_64-redhat-linux-gnu --host=x86_64-redhat-linux-gnu \
	--program-prefix= \
	--disable-dependency-tracking \
            --prefix=%{_libdir}/%{libname}          \
	--exec-prefix=/usr \
	    --bindir=%{_libdir}/%{libname}/bin      \
	    --sbindir=%{_libdir}/%{libname}/sbin    \
	    --sysconfdir=%{_sysconfdir}/%{namearch} \
	    --datadir=%{_libdir}/%{libname}/share   \
	    --includedir=%{_includedir}/%{namearch} \
	    --libdir=%{_libdir}/%{libname}/lib      \
	--libexecdir=/usr/libexec \
	--localstatedir=/var \
	--sharedstatedir=/var/lib \
	    --mandir=%{_mandir}/%{namearch}         \
	--infodir=/usr/share/info                   \
            --with-platform=optimized               \
            --enable-orterun-prefix-by-default      \
            --disable-mpi-fortran                   \
            --enable-contrib-no-build=vt            \
            --with-libevent=external                \
            --with-pmix=/usr                        \
            --with-hwloc=/usr

make %{?_smp_mflags}

%install
%make_install
find %{?buildroot} -name *.la -print0 | xargs -r0 rm -f


# Make the environment-modules file
mkdir -p %{buildroot}%{_sysconfdir}/modulefiles/mpi
# Since we're doing our own substitution here, use our own definitions.
sed 's#@LIBDIR@#%{_libdir}/%{libname}#;
     s#@ETCDIR@#%{_sysconfdir}/%{namearch}#;
     s#@FMODDIR@#%{_fmoddir}/%{libname}#;
     s#@INCDIR@#%{_includedir}/%{namearch}#;
     s#@MANDIR@#%{_mandir}/%{namearch}#;
     s#@PY2SITEARCH@#%{python_sitearch}/%{libname}#;
     s#@COMPILER@#%{variant}-'%{_arch}%{?_cc_name_suffix}'#g;
     s#@SUFFIX@#'%{?_cc_name_suffix}'_%{variant}#g' \
     <%{SOURCE301} \
     >%{buildroot}%{_sysconfdir}/modulefiles/mpi/%{namearch}

# make the rpm config file
install -Dpm 644 %{SOURCE302} %{buildroot}/%{macrosdir}/macros.%{namearch}

# Link the fortran module to proper location
mkdir -p %{buildroot}%{_fmoddir}/%{libname}
for mod in %{buildroot}%{_libdir}/%{libname}/lib/*.mod
do
  modname=$(basename $mod)
  ln -s ../../../%{libname}/lib/${modname} %{buildroot}/%{_fmoddir}/%{libname}/
done

mkdir -p %{buildroot}/%{python_sitearch}/%{libname}

# Link the pkgconfig files into the main namespace as well
mkdir -p %{buildroot}%{_libdir}/pkgconfig
cd %{buildroot}%{_libdir}/pkgconfig
ln -s ../%{libname}/lib/pkgconfig/*.pc .
cd -

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%dir %{_libdir}/%{libname}
%dir %{_sysconfdir}/%{namearch}
%dir %{_libdir}/%{libname}/bin
%dir %{_libdir}/%{libname}/lib
%dir %{_libdir}/%{libname}/lib/openmpi
%dir %{_mandir}/%{namearch}
%dir %{_mandir}/%{namearch}/man*
%dir %{_fmoddir}/%{libname}
%dir %{_sysconfdir}/modulefiles/mpi
%dir %{python_sitearch}/%{libname}
%config(noreplace) %{_sysconfdir}/%{namearch}/*
%{_libdir}/%{libname}/bin/mpi[er]*
%{_libdir}/%{libname}/bin/ompi*
%{_libdir}/%{libname}/bin/orte[-dr_]*
%{_libdir}/%{libname}/lib/*.so.*
%{_mandir}/%{namearch}/man1/mpi[er]*
%{_mandir}/%{namearch}/man1/ompi*
%{_mandir}/%{namearch}/man1/orte[-dr_]*
%{_mandir}/%{namearch}/man7/orte*
%{_mandir}/%{namearch}/man7/ompi*
%{_mandir}/%{namearch}/man7/opal*
%{_libdir}/%{libname}/lib/openmpi/*
%{_sysconfdir}/modulefiles/mpi/%{namearch}
%dir %{_libdir}/%{libname}/share
%dir %{_libdir}/%{libname}/share/openmpi
%{_libdir}/%{libname}/share/openmpi/amca-param-sets
%{_libdir}/%{libname}/share/openmpi/help*.txt
%{_libdir}/%{libname}/share/openmpi/mca-btl-openib-device-params.ini

%files devel
%dir %{_includedir}/%{namearch}
%{_libdir}/%{libname}/bin/mpi[cCf]*
%{_libdir}/%{libname}/bin/opal_*
%{_libdir}/%{libname}/bin/orte[cCf]*
%{_includedir}/%{namearch}/*
%{_fmoddir}/%{libname}/
%{_libdir}/%{libname}/lib/*.so
%{_libdir}/%{libname}/lib/pkgconfig/
%{_libdir}/pkgconfig/*.pc
%{_mandir}/%{namearch}/man1/mpi[cCf]*
%{_mandir}/%{namearch}/man1/opal_*
%{_mandir}/%{namearch}/man3/*
%{_libdir}/%{libname}/share/openmpi/openmpi-valgrind.supp
%{_libdir}/%{libname}/share/openmpi/*-wrapper-data.txt
%{macrosdir}/macros.%{namearch}

%changelog
* Sat Nov 09 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-9
- Install into /usr/lib64/openmpi/

* Tue Oct 29 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-8
- Build with PSM2

* Fri Oct 18 2019 Brian J. Murrell <brian.murrell@intel> - 3.0.0rc4-7
- Rebuild due to SUSE removing previous libhwloc5 RPM when
  updating to a newer hwloc
- Contrain hwloc-devel < 2.0.0 as OMPI doesn't support hwloc2

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
