# remirepo spec file for php-Smarty from:
#
# Fedora spec file for php-Smarty
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global gh_commit    4537d8aae6c4a26f5439bc3a05d3437d25c2c4d2
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     smarty-php
%global gh_project   smarty

Name:           php-Smarty
Summary:        Template/Presentation Framework for PHP
Version:        3.1.27
Release:        1%{?dist}

URL:            http://www.smarty.net
License:        LGPLv2+
Group:          Development/Libraries
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}-%{gh_short}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

# From composer.json
Requires:       php(language) >= 5.2.0
# From phpcompatinfo report for 3.1.21
Requires:       php-ctype
Requires:       php-date
Requires:       php-mbstring
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(smarty/smarty) = %{version}


%description
Although Smarty is known as a "Template Engine", it would be more accurately
described as a "Template/Presentation Framework." That is, it provides the
programmer and template designer with a wealth of tools to automate tasks
commonly dealt with at the presentation layer of an application. I stress the
word Framework because Smarty is not a simple tag-replacing template engine.
Although it can be used for such a simple purpose, its focus is on quick and
painless development and deployment of your application, while maintaining
high-performance, scalability, security and future growth.


%prep
%setup -qn %{gh_project}-%{gh_commit}


%build
# empty build section, nothing required


%install
rm -rf $RPM_BUILD_ROOT

# install smarty libs
install -d $RPM_BUILD_ROOT%{_datadir}/php/Smarty
cp -a libs/* $RPM_BUILD_ROOT%{_datadir}/php/Smarty/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license COPYING.lib
%doc README change_log.txt SMARTY*.txt
%doc INHERITANCE_RELEASE_NOTES.txt
%doc composer.json
%{_datadir}/php/Smarty


%changelog
* Thu Jun 18 2015 Remi Collet <remi@fedoraproject.org> - 3.1.27-1
- update to 3.1.27

* Tue Jun 16 2015 Remi Collet <remi@fedoraproject.org> - 3.1.25-1
- update to 3.1.25

* Sun May 24 2015 Remi Collet <remi@fedoraproject.org> - 3.1.24-2
- upstream patch for 'neq' regression
  https://github.com/smarty-php/smarty/issues/42

* Sun May 24 2015 Remi Collet <remi@fedoraproject.org> - 3.1.24-1
- update to 3.1.24

* Wed May 13 2015 Remi Collet <remi@fedoraproject.org> - 3.1.23-1
- update to 3.1.23

* Mon May 11 2015 Remi Collet <remi@fedoraproject.org> - 3.1.22-1
- update to 3.1.22

* Sat Oct 18 2014 Remi Collet <remi@fedoraproject.org> - 3.1.21-1
- update to 3.1.21
- sources from github

* Fri Oct 10 2014 Remi Collet <remi@fedoraproject.org> - 3.1.20-1
- update to 3.1.20

* Thu Jul 31 2014 Remi Collet <remi@fedoraproject.org> - 3.1.19-1
- backport 3.1.19 for remi repo
- fix license handling

* Wed Jul 30 2014 Johan Cwiklinski <johan AT x-tnd DOT be> - 3.1.19-1
- Last upstream release

* Sat May 10 2014 Johan Cwiklinski <johan AT x-tnd DOT be> - 3.1.18-1
- Last upstream release

* Sun Dec 22 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 3.1.16-1
- Last uypstream release

* Sun Dec 08 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 3.1.15-1
- Last upstream release

* Thu Aug 08 2013 Remi Collet <RPMS@FamilleCollet.com> - 3.1.14-1
- backport 3.1.14 for remi repo

* Thu Aug 08 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 3.1.14-1
- Last upstream release

* Tue Feb 12 2013 Remi Collet <RPMS@FamilleCollet.com> - 3.1.12-1
- backport 3.1.13 for remi repo

* Tue Feb 12 2013 Johan Cwiklinski <johan AT x-tnd DOT be> - 3.1.13-1
- Last upstream release
- Missing mbstring require

* Sun Nov 25 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 3.1.12-2
- Really fix requires (see bz #700179 comment #30)

* Sun Nov 25 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 3.1.12-1
- Update to 3.1.12
- Remove CVE-2012-4437 patch that has been included in that release
- Requires php-common instead of php

* Sat Sep 29 2012 Remi Collet <RPMS@FamilleCollet.com> - 3.1.12-1
- update to 3.1.12 for remi repo

* Thu Sep 20 2012 Jon Ciesla <limburgher@gmail.com> - 3.1.11-1
- Update to 3.1.11, patch for CVE-2012-4437, BZ 858989.

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.10-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Jun 22 2012 Johan Cwiklinski <johan AT x-tnd DOT be> - 3.1.10-1
- Update to 3.1.10

* Mon May 07 2012 Jon Ciesla <limburgher@gmail.com> - 3.1.8-1
- Update to 3.1.8, BZ 819162.

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.26-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Oct 11 2009 Christopher Stone <chris.stone@gmail.com> 2.6.26-1
- Upstream sync
- Update %%source0 and %%URL

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.25-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon May 25 2009 Christopher Stone <chris.stone@gmail.com> 2.6.25-1
- Upstream sync

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.6.20-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Nov 02 2008 Christopher Stone <chris.stone@gmail.com> 2.6.20-2
- Add security patch (bz #469648)
- Add RHL dist tag conditional for Requires

* Mon Oct 13 2008 Christopher Stone <chris.stone@gmail.com> 2.6.20-1
- Upstream sync

* Wed Feb 20 2008 Christopher Stone <chris.stone@gmail.com> 2.6.19-1
- Upstream sync
- Update %%license
- Fix file encoding

* Sun Apr 29 2007 Christopher Stone <chris.stone@gmail.com> 2.6.18-1
- Upstream sync

* Wed Feb 21 2007 Christopher Stone <chris.stone@gmail.com> 2.6.16-2
- Minor spec file changes/cleanups

* Fri Feb 09 2007 Orion Poplawski <orion@cora.nwra.com> 2.6.16-1
- Update to 2.6.16
- Install in /usr/share/php/Smarty
- Update php version requirement

* Tue May 16 2006 Orion Poplawski <orion@cora.nwra.com> 2.6.13-1
- Update to 2.6.13

* Tue Nov  1 2005 Orion Poplawski <orion@cora.nwra.com> 2.6.10-2
- Fix Source0 URL.

* Thu Oct 13 2005 Orion Poplawski <orion@cora.nwra.com> 2.6.10-1
- Initial Fedora Extras version
