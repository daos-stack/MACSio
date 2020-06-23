Name:    MACSio
Version: 1.1
Release: 1%{?commit:.git%{shortcommit}}%{?dist}
Summary: A Multi-purpose, Application-Centric, Scalable I/O Proxy Application

License: GPL
URL:     https://github.com/LLNL/MACSio
Source0: https://github.com/LLNL/%{name}/archive/v%{version}.tar.gz

BuildRequires: gcc, gcc-c++
%if 0%{?suse_version}
BuildRequires: gcc-fortran
%endif
BuildRequires: cmake
BuildRequires: json-cwx
BuildRequires: hdf5-devel%{?_isa}
BuildRequires: hdf5-mpich-devel%{?_isa}
BuildRequires: mpich-devel%{?_isa}

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

%prep
%setup -q

%build
%if (0%{?suse_version} >= 1500)
  module load gnu-mpich
%else
  module load mpi/mpich-%{_arch}
%endif
cmake -DCMAKE_INSTALL_PREFIX=%{_bindir} \
    -DWITH_JSON-CWX_PREFIX=/usr \
    -DENABLE_SILO_PLUGIN=OFF \
    -DENABLE_HDF5_PLUGIN=ON \
    -DWITH_HDF5_PREFIX=/usr/lib64/mpich
%if (0%{?suse_version} >= 1500)
sed -i -e s/H5pubconf.h/H5pubconf-64.h/ plugins/macsio_hdf5.c
%endif
make

%install
%{make_install}

%files
%license LICENSE
%{_bindir}/*

%changelog
* Tues Jun 23 2020 Phil Henderson <phillip.henderson@intel.com> - 1.1-1
- Initial version
