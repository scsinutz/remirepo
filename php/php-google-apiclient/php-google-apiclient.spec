# remirepo spec file for php-google-apiclient, from:
#
# Fedora spec file for php-google-apiclient
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#                         Adam Williamson <awilliam@redhat.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     google
%global github_name      google-api-php-client
%global github_version   1.1.4
%global github_commit    2adb5ba90612858d4add0342eee6b8b9aaca398d

%global composer_vendor  google
%global composer_project apiclient

# "php": ">=5.2.1"
%global php_min_ver 5.2.1

# Build using "--without tests" to disable tests
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Client library for Google APIs

Group:         Development/Libraries
License:       ASL 2.0
URL:           https://developers.google.com/api-client-library/php/
Source0:       https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: %{_bindir}/phpunit
## phpcompatinfo (computed from version 1.1.4)
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-json
BuildRequires: php-openssl
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

Requires:      ca-certificates
# composer.json
Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from version 1.1.4)
Requires:      php-curl
Requires:      php-date
Requires:      php-json
Requires:      php-openssl
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Google APIs Client Library for PHP provides access to many Google APIs.
It is designed for PHP client-application developers and offers simple,
flexible, powerful API access.

Optional:
* php-pecl-apcu
* php-pecl-memcache
* php-pecl-memcached

Examples are available in the %{name}-examples package.


%package examples

Summary:  Client library for Google APIs: Examples
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description examples
%{summary}


%prep
%setup -qn %{github_name}-%{github_commit}

: Unbundle CA cert
rm -f src/Google/IO/cacerts.pem
sed "s#dirname(__FILE__)\s*.\s*'/cacerts.pem'#'%{_sysconfdir}/pki/tls/certs/ca-bundle.crt'#" \
    -i src/Google/IO/{Stream,Curl}.php

: Update examples autoload require
sed "s#.*require.*autoload.*#require_once '%{phpdir}/Google/autoload.php';#" \
    -i examples/*.php


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Skip tests requiring network access
rm -f tests/general/ApiBatchRequestTest.php

: Run tests
%{_bindir}/phpunit

: Ensure unbundled CA cert is referenced
grep '%{_sysconfdir}/pki/tls/certs/ca-bundle.crt' --quiet \
    %{buildroot}%{phpdir}/Google/IO/{Curl,Stream}.php
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%{!?_licensedir:%global license %%doc}

%files
%defattr(-,root,root,-)
%license LICENSE
%doc *.md
%doc composer.json
%{phpdir}/Google

%files examples
%defattr(-,root,root,-)
%doc examples/*


%changelog
* Fri May 22 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.1.4-1
- Updated to 1.1.4 (BZ #1222260)
- Added spec license header
- Removed autoload patch
- Added option to build without tests

* Fri Jan 02 2015 Adam Williamson <awilliam@redhat.com> - 1.1.2-2
- update autoloader relocation patch to match latest upstream submission

* Sat Dec 20 2014 Adam Williamson <awilliam@redhat.com> - 1.1.2-1
- new upstream release 1.1.2
- relocate autoloader to make it work with systemwide installation

* Sat Dec 20 2014 Adam Williamson <awilliam@redhat.com> - 1.0.6-0.3.beta
- use new %%license directory
- add Packagist/Composer provide

* Fri Nov 07 2014 Adam Williamson <awilliam@redhat.com> - 1.0.6-0.2.beta
- apply CA trust store path substitution to Curl as well as Stream

* Fri Nov 07 2014 Adam Williamson <awilliam@redhat.com> - 1.0.6-0.1.beta
- new upstream release 1.0.6-beta

* Fri Feb 21 2014 Remi Collet <remi@fedoraproject.org> 1.0.3-0.2.beta
- backport for remi repo

* Wed Feb 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.3-0.2.beta
- Backported commit c6949531d2399f81a5e15caf256f156dd68e00e9 for OwnCloud
- Sub-packaged examples

* Sat Feb 08 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.3-0.1.beta
- Initial package
