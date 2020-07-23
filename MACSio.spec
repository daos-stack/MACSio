%global with_mpich 1
%global with_openmpi3 1

%if %{with_mpich}
%global mpi_list mpich
%endif
%if %{with_openmpi3}
%global mpi_list %{?mpi_list} openmpi3
%endif

%if (0%{?suse_version} >= 1500)
%global module_load() if [ "%{1}" == "openmpi3" ]; then module load gnu-openmpi; else module load gnu-%{1}; fi
%else
%global module_load() module load mpi/%{1}-%{_arch}
%endif

Name:    MACSio
Version: 1.1
Release: 2%{?commit:.git%{shortcommit}}%{?dist}
Summary: A Multi-purpose, Application-Centric, Scalable I/O Proxy Application

License: GPL
URL:     https://github.com/LLNL/MACSio
Source0: https://github.com/LLNL/%{name}/archive/v%{version}.tar.gz

%if 0%{?suse_version}
BuildRequires: gcc-fortran
BuildRequires: lua-lmod
BuildRequires: gcc, gcc-c++
%endif
BuildRequires: cmake
BuildRequires: json-cwx
BuildRequires: hdf5-devel%{?_isa}
Requires: json-cwx

%if %{with_mpich}
%package mpich
Summary: A Multi-purpose, Application-Centric, Scalable I/O Proxy Application for MPICH
BuildRequires: hdf5-mpich-devel%{?_isa}
BuildRequires: mpich-devel%{?_isa}

%description mpich
MACSio for MPICH
%endif

%if %{with_openmpi3}
%package openmpi3
Summary: A Multi-purpose, Application-Centric, Scalable I/O Proxy Application for OpenMPI3
BuildRequires: hdf5-openmpi3-devel%{?_isa}
BuildRequires: openmpi3-devel%{?_isa}

%description openmpi3
MACSio for OpenMPI3
%endif

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

%prep
%setup -q

%build
for mpi in %{?mpi_list}
do
  mkdir $mpi
  pushd $mpi
  %module_load $mpi
  cmake -DCMAKE_INSTALL_PREFIX=%{_bindir}/$mpi \
    -DWITH_JSON-CWX_PREFIX=%{_usr} \
    -DENABLE_SILO_PLUGIN=OFF \
    -DENABLE_HDF5_PLUGIN=ON \
    -DWITH_HDF5_PREFIX=%{_libdir}/$mpi
%if (0%{?suse_version} >= 1500)
  sed -i -e s/H5pubconf.h/H5pubconf-64.h/ plugins/macsio_hdf5.c
%endif
  make
  module purge
  popd
done

%install
for mpi in %{?mpi_list}
do
  %module_load $mpi
  make -C $mpi install DESTDIR=%{buildroot}
  module purge
done

%files
%if %{with_mpich}
%license LICENSE
%{_bindir}/mpich/*
%endif
%if %{with_openmpi3}
%license LICENSE
%{_bindir}/openmpi3/*
%endif

%changelog
* Thu Jul 23 2020 Phil Henderson <phillip.henderson@intel.com> - 1.1-2
- Renamed existing package to MACSio-mpich and added the MACSio-openmpi3 package

* Wed Jun 24 2020 Phil Henderson <phillip.henderson@intel.com> - 1.1-1
- Initial version
