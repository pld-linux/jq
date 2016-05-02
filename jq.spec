#
# Conditional build:
%bcond_without	tests		# build without tests

%ifnarch %{ix86} %{x8664}
%undefine	with_tests
%endif

Summary:	Command-line JSON processor
Name:		jq
Version:	1.5
Release:	1
License:	MIT and ASL 2.0 and CC-BY and GPLv3
Group:		Applications/Text
Source0:	https://github.com/stedolan/jq/releases/download/%{name}-%{version}/jq-%{version}.tar.gz
# Source0-md5:	0933532b086bd8b6a41c1b162b1731f9
Patch0:		static.patch
URL:		https://stedolan.github.io/jq/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	bison
BuildRequires:	flex
BuildRequires:	libtool
BuildRequires:	oniguruma-devel
%if %{with tests}
BuildRequires:	valgrind
%endif
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
lightweight and flexible command-line JSON processor

jq is like sed for JSON data - you can use it to slice and filter and
map and transform structured data with the same ease that sed, awk,
grep and friends let you play with text.

It is written in portable C, and it has zero runtime dependencies.

jq can mangle the data format that you have into the one that you want
with very little effort, and the program to do so is often shorter and
simpler than you'd expect.

%package libs
Summary:	Shared libraries for jq
Group:		Libraries

%description libs
Shared libraries for jq.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Development files for %{name}

%prep
%setup -q
%patch0 -p1

%build
%{__aclocal} -I config/m4
%{__libtoolize}
%{__autoconf}
%{__automake}
%configure \
	--disable-static \
	--disable-all-static \
	--disable-silent-rules

%{__make}

# Docs already shipped in jq's tarball.
# In order to build the manual page, it
# is necessary to install rake, rubygem-ronn
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
%doc README README.md AUTHORS COPYING
%attr(755,root,root) %{_bindir}/jq
%{_mandir}/man1/jq.1*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libjq.so.*.*.*
%ghost %{_libdir}/libjq.so.1

%files devel
%defattr(644,root,root,755)
%{_includedir}/jq.h
%{_includedir}/jv.h
%{_libdir}/libjq.so
