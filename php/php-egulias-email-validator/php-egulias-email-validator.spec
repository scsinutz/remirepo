#
# RPM spec file for php-egulias-email-validator
#
# Copyright (c) 2014-2015 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     egulias
%global github_name      EmailValidator
%global github_version   1.2.7
%global github_commit    af9417f765623429c9d2a200f0159537e08d1ef3

%global composer_vendor  egulias
%global composer_project email-validator

# "php": ">= 5.3.3"
%global php_min_ver 5.3.3
# "doctrine/lexer": "~1.0"
%global doctrine_lexer_min_ver 1.0
%global doctrine_lexer_max_ver 2.0

# Build using "--without tests" to disable tests
%global with_tests  %{?_without_tests:0}%{!?_without_tests:1}

%{!?phpdir:     %global phpdir     %{_datadir}/php}
%{!?__phpunit:  %global __phpunit  %{_bindir}/phpunit}

Name:          php-%{composer_vendor}-%{composer_project}
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A library for validating emails

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:     noarch
%if %{with_tests}
BuildRequires: php-phpunit-PHPUnit
# composer.json
BuildRequires: php(language)                >= %{php_min_ver}
BuildRequires: php-composer(doctrine/lexer) >= %{doctrine_lexer_min_ver}
BuildRequires: php-composer(doctrine/lexer) <  %{doctrine_lexer_max_ver}
# phpcompatinfo (computed from version 1.2.7)
BuildRequires: php-filter
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-spl
%endif

# composer.json
Requires:      php(language)                >= %{php_min_ver}
Requires:      php-composer(doctrine/lexer) >= %{doctrine_lexer_min_ver}
Requires:      php-composer(doctrine/lexer) <  %{doctrine_lexer_max_ver}
# phpcompatinfo (computed from version 1.2.7)
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl

# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
%{summary}.


%prep
%setup -qn %{github_name}-%{github_commit}

# W: wrong-file-end-of-line-encoding /usr/share/doc/php-egulias-email-validator/README.md
sed -i 's/\r$//' README.md


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -pm 0755 %{buildroot}%{phpdir}
cp -rp src/* %{buildroot}%{phpdir}/


%check
%if %{with_tests}
# Create autoloader
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php

spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    @include_once $src;
});
AUTOLOAD

# Skip testValidEmailsWithWarningsCheck and testInvalidEmailsWithDnsCheckAndStrictMode
# because Koji does not have network access so assertEquals(expected_warnings, actual_warnings)
# fails because EmailValidator::DNSWARN_NO_RECORD is not an expected warning
sed -e 's/function testValidEmailsWithWarningsCheck/function SKIP_testValidEmailsWithWarningsCheck/' \
    -e 's/function testInvalidEmailsWithDnsCheckAndStrictMode/function SKIP_testInvalidEmailsWithDnsCheckAndStrictMode/' \
    -i tests/egulias/Tests/EmailValidator/EmailValidatorTest.php

%{__phpunit} --include-path %{buildroot}%{phpdir}
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%dir %{phpdir}/Egulias
     %{phpdir}/Egulias/EmailValidator


%changelog
* Mon Jan 05 2015 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.7-1
- Updated to 1.2.7 (BZ #1178809)

* Sun Dec 07 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.6-1
- Updated to 1.2.6 (BZ #1171051)

* Sun Nov 09 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.5-1
- Updated to 1.2.5

* Thu Nov  6 2014 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- backport for remi repository

* Mon Nov 03 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.4-1
- Updated to 1.2.4

* Mon Oct 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.3-1
- Updated to 1.2.3

* Wed Sep 10 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.2-1
- Initial package
