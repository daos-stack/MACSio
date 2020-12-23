%global daos_major 0

%global with_mpich 1
%global with_openmpi3 1

%if %{with_mpich}
%global mpi_list mpich
%endif
%if %{with_openmpi3}
%global mpi_list %{?mpi_list} openmpi3
%endif

%if (0%{?suse_version} >= 1500)
%global module_load() if [ "%{1}" == "openmpi3" ]; then MODULEPATH=/usr/share/modules module load gnu-openmpi; else MODULEPATH=/usr/share/modules module load gnu-%{1}; fi
%global mpi_libdir %{_libdir}/mpi/gcc
%global cmake cmake
%else
%global module_load() module load mpi/%{1}-%{_arch}
%global mpi_libdir %{_libdir}
%global cmake cmake3
%endif

Name:    MACSio
Version: 1.1
Release: 5%{?commit:.git%{shortcommit}}%{?dist}
Summary: A Multi-purpose, Application-Centric, Scalable I/O Proxy Application

License: GPL
URL:     https://github.com/LLNL/MACSio
Source0: https://github.com/LLNL/%{name}/archive/v%{version}.tar.gz

%if (0%{?suse_version} >= 1500)
BuildRequires: gcc-fortran
BuildRequires: cmake >= 3.1
BuildRequires: lua-lmod
%else
BuildRequires: cmake3 >= 3.1
BuildRequires: Lmod
%endif
BuildRequires: gcc, gcc-c++
BuildRequires: json-cwx
BuildRequires: hdf5-devel%{?_isa}
Requires: json-cwx

%description
MACSio is being developed to fill a long existing void in co-design proxy
applications that allow for I/O performance testing and evaluation of tradeoffs
in data models, I/O library interfaces and parallel I/O paradigms for
multi-physics, HPC applications.

Two key design features of MACSio set it apart from existing I/O proxy
applications and benchmarking tools. The first is the level of abstraction (LOA)
at which MACSio is being designed to operate. The second is the degree of
flexibility MACSio is being designed to provide in driving an HPC I/O workload
through parameterized, user-defined data objects and a variety of parallel I/O
paradigms and I/O interfaces.

Combined, these features allow MACSio to closely mimic I/O workloads for a wide
variety of real applications and, in particular, multi-physics applications
where data object distribution and composition vary dramatically both within and
across parallel tasks. These data objects can then be marshaled using one or
more I/O interfaces and parallel I/O paradigms, allowing for direct comparisons
of software interfaces, parallel I/O paradigms, and file system technologies
with the same set of customizable data objects.

We hope MACSio helps to put the MAX in scalable I/O performance ;)

The name "MACSio" is pronounced max-eee-oh.


%if %{with_mpich}
%package mpich
Summary: MACSio for MPICH
BuildRequires: hdf5-mpich-devel%{?_isa}
BuildRequires: mpich-devel%{?_isa}
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: %{name}-mpich2-daos-%{daos_major} = %{version}-%{release}

%description mpich
MACSio for MPICH
%endif

%if %{with_openmpi3}
%package openmpi3
Summary: MACSio for OpenMPI 3
BuildRequires: hdf5-openmpi3-devel%{?_isa}
BuildRequires: openmpi3-devel%{?_isa}
Requires: %{name}%{?_isa} = %{version}-%{release}
Provides: %{name}-openmpi3-daos-%{daos_major} = %{version}-%{release}

%description openmpi3
MACSio for OpenMPI 3
%endif

%prep
%setup -q

%build
%if (0%{?suse_version} >= 1500)
  sed -i -e s/H5pubconf.h/H5pubconf-64.h/ plugins/macsio_hdf5.c
%endif
for mpi in %{?mpi_list}
do
  mkdir $mpi
  pushd $mpi
  %module_load $mpi
  %{cmake} -DCMAKE_INSTALL_PREFIX=%{mpi_libdir}/$mpi/bin \
    -DWITH_JSON-CWX_PREFIX=%{prefix} \
    -DENABLE_SILO_PLUGIN=OFF \
    -DENABLE_HDF5_PLUGIN=ON \
    -DWITH_HDF5_PREFIX=%{mpi_libdir}/$mpi \
    ..
  %{make_build}
  module purge
  popd
done

%install
for mpi in %{?mpi_list}
do
  %module_load $mpi
  %{make_install} -C $mpi
  module purge
done

%files
%license LICENSE
%if %{with_mpich}
%files mpich
%{mpi_libdir}/mpich/bin/*
%endif
%if %{with_openmpi3}
%files openmpi3
%{mpi_libdir}/openmpi3/bin/*
%endif

%changelog
* Wed Dec 23 2020  Maureen Jean <maureen.jean@intel.com> - 1.1-5
- update to build with latest hdf5

* Tue Nov 17 2020  Maureen Jean <maureen.jean@intel.com> - 1.1-4
- update to build with latest hdf5

* Mon Aug 24 2020 Phil Henderson <phillip.henderson@intel.com> - 1.1-3
- Enable build with SLES15.2

* Thu Jul 23 2020 Phil Henderson <phillip.henderson@intel.com> - 1.1-2
- Added mpich and openmpi3 packages

* Wed Jun 24 2020 Phil Henderson <phillip.henderson@intel.com> - 1.1-1
- Initial version
