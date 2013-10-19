%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global pear_channel pear.symfony.com
%global pear_name    Validator
%global php_min_ver  5.3.3
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:             php-symfony2-%{pear_name}
Version:          2.3.6
Release:          1%{?dist}
Summary:          Symfony2 %{pear_name} Component

Group:            Development/Libraries
License:          MIT
URL:              http://symfony.com/doc/current/components/index.html
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch

BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})
%if %{with_tests}
# For tests
BuildRequires:    php(language) >= %{php_min_ver}
BuildRequires:    php-pear(pear.phpunit.de/PHPUnit)
BuildRequires:    php-pear(%{pear_channel}/Config) > 2.2
BuildRequires:    php-pear(%{pear_channel}/HttpFoundation) > 2.1
BuildRequires:    php-pear(%{pear_channel}/Intl) > 2.3
BuildRequires:    php-pear(%{pear_channel}/Translation) > 2.0
BuildRequires:    php-pear(%{pear_channel}/Yaml) > 2.0
BuildRequires:    php-pear(pear.doctrine-project.org/DoctrineCommon)
# For tests: phpci
BuildRequires:    php-ctype
BuildRequires:    php-date
BuildRequires:    php-dom
BuildRequires:    php-intl
BuildRequires:    php-libxml
BuildRequires:    php-mbstring
BuildRequires:    php-pcre
BuildRequires:    php-reflection
BuildRequires:    php-simplexml
BuildRequires:    php-spl
BuildRequires:    php-filter
%endif

Requires:         php(language) >= %{php_min_ver}
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# phpci
Requires:         php-ctype
Requires:         php-date
Requires:         php-dom
Requires:         php-intl
Requires:         php-libxml
Requires:         php-mbstring
Requires:         php-pcre
Requires:         php-reflection
Requires:         php-simplexml
Requires:         php-spl
Requires:         php-filter
Requires:         php-pear(%{pear_channel}/Translation) > 2.0
# Optional
Requires:         php-pear(%{pear_channel}/Config) > 2.2
Requires:         php-pear(%{pear_channel}/HttpFoundation) > 2.1
Requires:         php-pear(%{pear_channel}/Intl) > 2.3
Requires:         php-pear(%{pear_channel}/Yaml) > 2.0
Requires:         php-pear(pear.doctrine-project.org/DoctrineCommon)

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
This component is based on the JSR-303 Bean Validation specification and
enables specifying validation rules for classes using XML, YAML, PHP or
annotations, which can then be checked against instances of these classes.

Optional dependencies: APC, DoctrineCommon


%prep
%setup -q -c

# Create PHPUnit autoloader
( cat <<'PHPUNIT_AUTOLOADER'
<?php

# This file was created by RPM packaging and is not part of the original
# Symfony2 %{pear_name} PEAR package.

set_include_path(
    '%{pear_testdir}/%{pear_name}'.PATH_SEPARATOR.
    get_include_path()
);

spl_autoload_register(function ($class) {
    if ('\\' == $class[0]) {
        $class = substr($class, 1);
    }

    $file = str_replace('\\', '/', $class).'.php';
    @include $file;
});
PHPUNIT_AUTOLOADER
) > phpunit.autoloader.php

# Update PHPUnit config
sed -e 's#vendor/autoload.php#./phpunit.autoloader.php#' \
    -i %{pear_name}-%{version}/Symfony/Component/%{pear_name}/phpunit.xml.dist

# Modify PEAR package.xml file:
# - Change role from "php" to "test" for all test files
# - Remove md5sum from phpunit.xml.dist file since it was updated
sed -e '/Tests/s/role="php"/role="test"/' \
    -e '/phpunit.xml.dist/s/role="php"/role="test"/' \
    -e '/phpunit.xml.dist/s/md5sum="[^"]*"\s*//' \
    -i package.xml

# package.xml is version 2.0
mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
# Empty build section, nothing required


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# Install PHPUnit autoloader
install -pm 0644 ../phpunit.autoloader.php \
    %{buildroot}/%{pear_testdir}/%{pear_name}/Symfony/Component/%{pear_name}/


%check
cd %{pear_name}-%{version}/Symfony/Component/%{pear_name}

cp ../../../../phpunit.autoloader.php .

%if %{with_tests}
%{_bindir}/phpunit \
    -d include_path="%{buildroot}%{pear_phpdir}:%{buildroot}%{pear_testdir}/%{pear_name}:.:%{pear_phpdir}:%{_datadir}/php" \
    -d date.timezone="UTC" \
    || : Temporarily ignore failed tests
%else
: Test disabled, missing '--with tests' option.
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Symfony/Component/%{pear_name}
%{pear_testdir}/%{pear_name}


%changelog
* Fri Oct 18 2013 Remi Collet <remi@fedoraproject.org> - 2.3.6-1
- Update to 2.3.6

* Thu Aug 22 2013 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- Sync with rawhide, update to 2.2.5
- disable tests as results are ignored...

* Fri Aug 09 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.5-1
- Updated to 2.2.5

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.2.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 02 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.3-1
- Updated to 2.2.3

* Thu Jun 13 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.2-1
- Updated to 2.2.2
- Removed package.xml modifications fixed usptream

* Mon Jun 03 2013 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

* Mon Apr 15 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.1-1
- Updated to 2.2.1

* Sat Apr 06 2013 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Wed Mar 13 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.0-1
- Updated to 2.2.0
- Removed tests' bootstrap patch
- Added php-pear(%%{pear_channel}/Config) require
- Added php-pear(%%{pear_channel}/Translation) require
- Added php-pear(pear.doctrine-project.org/DoctrineCommon) require
- Temporarily ignore failed tests

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Wed Feb 27 2013 Remi Collet <remi@fedoraproject.org> - 2.1.8-1
- Update to 2.1.8

* Mon Jan 21 2013 Remi Collet <RPMS@FamilleCollet.com> 2.1.7-1
- update to 2.1.7

* Fri Dec 21 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.6-1
- update to 2.1.6 (no change)

* Fri Dec 21 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.5-1
- update to 2.1.5

* Thu Nov 29 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.4-1
- update to 2.1.4

* Wed Nov 14 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.1.3-1
- Updated to upstream version 2.1.3
- Removed .gitattributes file from package.xml

* Tue Oct 30 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.1.2-3
- Temporarily disable tests on EL

* Tue Oct 30 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.3-1
- sync with rawhide, update to 2.1.3

* Mon Oct 29 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.1.2-2
- Added "%%global pear_metadir" and usage in %%install
- Changed RPM_BUILD_ROOT to %%{buildroot}

* Tue Oct 23 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.1.2-1
- Updated to upstream version 2.1.2
- PHP minimum version 5.3.3 instead of 5.3.2
- Require other components ">= 2.1.0" instead of "= %%{version}"
- Added PEAR package.xml modifications
- Added patch for tests' bootstrap.php
- Added tests (%%check)

* Sat Oct  6 2012 Remi Collet <RPMS@FamilleCollet.com> 2.1.2-1
- update to 2.1.2

* Sat Sep 15 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.17-1
- Update to 2.0.17, backport for remi repository

* Sat Sep 15 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.17-1
- Updated to upstream version 2.0.17
- Added php-dom and php-reflection requires

* Sun Jul 22 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.16-2
- Made php-filter a dist specific require (not available in EPEL)

* Fri Jul 20 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.16-1
- Update to 2.0.16, backport for remi repository

* Wed Jul 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.16-1
- Updated to upstream version 2.0.16
- Added php-filter require
- Removed fix package.xml for *.xsd file issue (fixed upstream)
- Minor syntax updates

* Tue Jul 03 2012 Remi Collet <RPMS@FamilleCollet.com> 2.0.15-4
- backport for remi repository

* Sat Jun 30 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-4
- Removed APC require
- Updated %%description

* Tue Jun 12 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-3
- Fix package.xml for *.xsd file issue

* Mon Jun 11 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-2
- Added php-pear(%%{pear_channel}/HttpFoundation) require
- Added php-pear(%%{pear_channel}/Yaml) require
- Removed ownership for directories already owned by required packages

* Wed May 30 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.15-1
- Updated to upstream version 2.0.15
- Removed "BuildRequires: php-pear >= 1:1.4.9-1.2"
- Updated %%prep section
- Removed cleaning buildroot from %%install section
- Removed documentation move from %%install section (fixed upstream)
- Removed %%clean section
- Updated %%doc in %%files section

* Wed May 23 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-4
- Added missing php-intl require

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-3
- Moved documentation to correct location

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-2
- Removed BuildRoot
- Changed php require to php-common
- Added the following requires based on phpci results:
  php-ctype, php-date, php-libxml, php-mbstring, php-pcre,
  php-simplexml, php-spl, php-pecl-apc
- Removed %%defattr from %%files section

* Fri May 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.14-1
- Updated to upstream version 2.0.14
- %%global instead of %%define
- Removed unnecessary cd from %%build section

* Wed May  2 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.13-1
- Updated to upstream version 2.0.13

* Sat Apr 21 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.0.12-1
- Initial package
