#
# Conditional build:
%bcond_without	static_libs	# static library
%bcond_without	tests		# check target
%bcond_with	tests_valgrind	# use valgrind for tests (suspectible to glibc false positives)

Summary:	Command-line JSON processor
Summary(pl.UTF-8):	Procesor JSON działający z linii poleceń
Name:		jq
Version:	1.8.1
Release:	1
License:	MIT, Apache, CC-BY, GPL v3
Group:		Applications/Text
#Source0Download: https://github.com/jqlang/jq/releases
Source0:	https://github.com/jqlang/jq/releases/download/%{name}-%{version}/jq-%{version}.tar.gz
# Source0-md5:	ea4bb241cd9c625b43b0988776db1e03
Patch0:		tests-no-pty.patch
URL:		https://jqlang.github.io/jq/
# for --enable-year2038
BuildRequires:	autoconf >= 2.72
BuildRequires:	automake >= 1:1.11.2
BuildRequires:	bison >= 3
BuildRequires:	flex
BuildRequires:	libtool >= 2:2
BuildRequires:	oniguruma-devel
BuildRequires:	rpmbuild(macros) >= 1.527
%{?with_tests_valgrind:BuildRequires:	valgrind}
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
lightweight and flexible command-line JSON processor.

jq is like sed for JSON data - you can use it to slice and filter and
map and transform structured data with the same ease that sed, awk,
grep and friends let you play with text.

It is written in portable C, and it has zero runtime dependencies.

%description -l pl.UTF-8
Lekki i elastyczny procesor JSON działający z linii poleceń.

jq jest odpowiednikiem seda dla danych JSON - można go używać do
podziału, filtrowania, odwzorowywania i przekształceń danych
strukturalnych tak samo łatwo, jak programy sed, awk, grep i podobne
pozwalają bawić się tekstem.

Jest napisany w przenośnym C i nie ma dodatkowych zależności.

%package libs
Summary:	Shared jq library
Summary(pl.UTF-8):	Biblioteka współdzielona jq
Group:		Libraries

%description libs
Shared jq library.

%description libs -l pl.UTF-8
Biblioteka współdzielona jq.

%package devel
Summary:	Header files for jq library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki jq
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for jq library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki jq.

%package static
Summary:	Static jq library
Summary(pl.UTF-8):	Statyczna biblioteka jq
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static jq library.

%description static -l pl.UTF-8
Statyczna biblioteka jq.

%prep
%setup -q
%patch -P0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4 -I config/m4
%{__autoconf}
%{__automake}
%configure \
	--disable-docs \
	%{!?with_static_libs:--disable-static} \
	--disable-all-static \
	--disable-silent-rules \
	--enable-year2038 \
	%{__enable_disable tests_valgrind valgrind}

echo -e '#!/bin/sh\necho "'%{version}'"' > scripts/version

%{__make}

# Docs already shipped in jq's tarball.
# In order to build the manual page, it
# is necessary to install rake, rubygem-ronn, bonsai
# and do the following steps:
#
# # yum install rake rubygem-ronn
# $ cd docs/
# $ curl -L https://get.rvm.io | bash -s stable --ruby=1.9.3
# $ source $HOME/.rvm/scripts/rvm
# $ bundle install
# $ cd ..
# $ ./configure
# $ make real_docs

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libjq.la

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS.md README.md
%attr(755,root,root) %{_bindir}/jq
%{_mandir}/man1/jq.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjq.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libjq.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjq.so
%{_includedir}/jq.h
%{_includedir}/jv.h
%{_pkgconfigdir}/libjq.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libjq.a
%endif
