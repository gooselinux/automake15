Summary:    A GNU tool for automatically creating Makefiles
Name:       automake15
Version:    1.5
Release:    27%{?dist}.1
License:    GPLv2+
Group:      Development/Tools
URL:        http://sources.redhat.com/automake
Source:     ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.gz
Source10:   filter-provides-automake.sh
Source11:   filter-requires-automake.sh
Patch1:     automake-1.5-depout-mf.patch
Patch2:     automake15-versioning.patch
Patch3:     automake15-autoconf253.patch
Patch4:     automake-1.5-subdirs-89619.patch
Patch5:     dirnames.test-1.6.patch
Patch6:     automake-1.5-ppc-ccnoco-test-91853.patch
Patch7:     automake-1.5-tailfix.patch
Patch8:     automake-1.5-depconf2.patch
Patch9:     automake-1.5-info.patch
Patch10:    automake-1.5-noautotools.patch
Patch11:    automake-1.5-CVE-2009-4029.patch
Buildrequires:  autoconf, bison, texinfo
Requires(post):  /sbin/install-info
Requires(preun): /sbin/install-info
BuildArch:  noarch
Buildroot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%define _use_internal_dependency_generator 0
%define __find_provides %{SOURCE10}
%define __find_requires %{SOURCE11}

%description
Automake is a tool for automatically generating
`Makefile.in' files compliant with the GNU Coding Standards.

This package contains Automake 1.5, an older version of Automake.
You should install it if you need to run automake in a project that
has not yet been updated to work with newer versions of Automake.

# run "make check" by default
%{?_without_check: %define _without_check 1}
%{!?_without_check: %define _without_check 0}

%prep
%setup -q -n automake-%{version}
# %patch1 -p1 -b .makefile
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%ifarch ppc ppc64
%patch6 -p1
%endif
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1 -b .noautotools
%patch11 -p1

%build
mv automake.texi automake15.texi
rm -f automake.info*
touch -r configure.noautotools configure
#touch -r configure.in.orig configure.in
# patch 2 touches configure.in
autoconf
./configure --program-suffix=-%{version} --prefix=%{_prefix} \
   --mandir=%{_mandir} --infodir=%{_infodir} --bindir=%{_bindir} \
   --datadir=%{_datadir}
make %{?_smp_mflags}

%check
%if ! %{_without_check}
  make check
%endif

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

# create this dir empty so we can own it
mkdir -p $RPM_BUILD_ROOT%{_datadir}/aclocal

%post
/sbin/install-info %{_infodir}/%{name}.info %{_infodir}/dir || :

%preun
if [ "$1" = 0 ]; then
    /sbin/install-info --delete %{_infodir}/%{name}.info %{_infodir}/dir || :
fi

%clean
#rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root)
%doc COPYING
%{_bindir}/*-%{version}
%{_infodir}/*
%{_datadir}/automake-%{version}
%{_datadir}/aclocal-%{version}
%dir %{_datadir}/aclocal

%changelog
* Tue Feb 16 2010 Karsten Hopp <karsten@redhat.com> 1.5-27.1
- fix CVE-2009-4029

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-27
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Mon Feb 23 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.5-26
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Oct 02 2008 Karsten Hopp <karsten@redhat.com> 1.5-25 
- fix build error

* Mon Jul 14 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5-24
- fix patch2 to apply with fuzz=0
- fix license tag

* Wed Mar 05 2008 Karsten Hopp <karsten@redhat.com> 1.5-23
- fix source URL

* Mon Apr 16 2007 Karsten Hopp <karsten@redhat.com> 1.5-22
- update subdirs patch (#225299)
- don't run autotools during build

* Mon Mar 19 2007 Karsten Hopp <karsten@redhat.com> 1.5-21
- remove erroneous provides (#224569)

* Thu Feb 22 2007 Karsten Hopp <karsten@redhat.com> 1.5-20
- add missing buildrequirement texinfo (#229572)

* Tue Feb 20 2007 Karsten Hopp <karsten@redhat.com> 1.5-19
- use ./configure 

* Mon Feb 19 2007 Karsten Hopp <karsten@redhat.com> 1.5-18
- use spaces instead of tabs
- remove trailing dot from summary
- use make install DESTDIR=...
- drop requirement on perl
- install info files as automake15.info


* Tue Jan 30 2007 Karsten Hopp <karsten@redhat.com> 1.5-17
- drop obsolete check

* Fri Jun 09 2006 Karsten Hopp <karsten@redhat.de> 1.5-16
- filter self provided dependencies

* Thu Jun 01 2006 Karsten Hopp <karsten@redhat.de> 1.5-15
- buildrequire bison for self tests

* Mon Dec 19 2005 Karsten Hopp <karsten@redhat.de> 1.5-14
- fix insthook test:
  tail needs parameters '-n +NUMLINES' instead of '+NUMLINES' now

* Fri Dec 09 2005 Jesse Keating <jkeating@redhat.com>
- rebuilt

* Tue Sep 28 2004 Warren Togami <wtogami@redhat.com> - 1.5-13
- trim docs

* Thu Sep 23 2004 Daniel Reed <djr@redhat.com> - 1.5-11
- rebuilt for dist-fc3

* Fri Feb 13 2004 Elliot Lee <sopwith@redhat.com>
- rebuilt

* Fri Jun  6 2003 Jens Petersen <petersen@redhat.com> - 1.5-9
- update ccnoco.test to version from 1.6.3 for ppc (#91853)

* Fri Apr 25 2003 Jens Petersen <petersen@redhat.com> - 1.5-8
- add patch from 1.6 branch to fix #89619 [thanks to hjl@gnu.org]
- run build tests by default
- add --without-check build option
- update dirname.test to 1.6 version so it doesn't fail
- buildrequire autoconf
- don't look for autoconf253 files in missing
- add info files to doc dir
- update description

* Wed Jan 22 2003 Tim Powers <timp@redhat.com>
- rebuilt

* Thu Dec 12 2002 Elliot Lee <sopwith@redhat.com> 1.5-5
- Remove unpackaged files

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Wed Mar 27 2002 Jens Petersen <petersen@redhat.com> 1.5-2
- make "missing" look for versioned auto* scripts by default (#61591).
  Suggested by enrico.scholz@informatik.tu-chemnitz.de

* Thu Feb 28 2002 Jens Petersen <petersen@redhat.com> 1.5-1
- new package based on automake-1.5
- version datadir and no longer make symlinks in bindir
- exclude info files

* Wed Jan 23 2002 Jens Petersen <petersen@redhat.com> 1.5-8
- better aclocal versioning

* Wed Jan 23 2002 Jens Petersen <petersen@redhat.com> 1.5-7
- don't version datadir/automake

* Tue Jan 15 2002 Jens Petersen <petersen@redhat.com> 1.5-6
- version suffix programs and data directories
- own symlinks to programs and /usr/share/aclocal

* Wed Jan 09 2002 Tim Powers <timp@redhat.com> 1.5-5
- automated rebuild

* Wed Jan  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.5-4
- Completely back out the fix for #56624 for now, it causes more problems
  than it fixes in either form.

* Wed Jan  9 2002 Bernhard Rosenkraenzer <bero@redhat.com> 1.5-3
- Don't use AS_DIRNAME, it doesn't work.

* Tue Jan  7 2002 Jens Petersen <petersen@redhat.com> 1.5-2
- Patch depout.m4 to handle makefiles passed to make with "-f" (#56624)

* Tue Sep 18 2001 Bernhard Rosenkraenzer <bero@redhat.com> 1.5-1
- Update to 1.5 - much better to coexist with autoconf 2.52...
- Fix specfile
- No patches

* Fri Aug 24 2001 Jens Petersen <petersen@redhat.com> - 1.4p5-2
- dont raise error when there is source in a subdirectory (bug #35156).
  This was preventing automake from working in binutuls/gas 
  [patch from HJ Lu <hjl@gnu.org>]
- format long lines of output properly with backslash + newlines as in 1.4
  (bug #35259) [patch from HJ Lu <hjl@gnu.org>]

* Sat Jul 21 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- 1.4-p5, fixes #48788

* Tue Jun 12 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- add the patch from #20559
- really update to 1.4-p4

* Mon Jun 11 2001 Florian La Roche <Florian.LaRoche@redhat.de>
- update to 1.4-p4

* Sat May 12 2001 Owen Taylor <otaylor@redhat.com>
- Version 1.4-p1 to work with libtool-1.4

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Mon Jun  5 2000 Jeff Johnson <jbj@redhat.com>
- FHS packaging.

* Fri Feb 04 2000 Nalin Dahyabhai <nalin@redhat.com>
- fix bug #8870

* Sat Aug 21 1999 Jeff Johnson <jbj@redhat.com>
- revert to pristine automake-1.4.

* Mon Mar 22 1999 Preston Brown <pbrown@redhat.com>
- arm netwinder patch

* Wed Feb 24 1999 Preston Brown <pbrown@redhat.com>
- Injected new description and group.

* Mon Feb  8 1999 Jeff Johnson <jbj@redhat.com>
- add patches from CVS for 6.0beta1

* Sun Jan 17 1999 Jeff Johnson <jbj@redhat.com>
- update to 1.4.

* Mon Nov 23 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.3b.
- add URL.

* Fri Apr 24 1998 Prospector System <bugs@redhat.com>
- translations modified for de, fr, tr

* Tue Apr 07 1998 Erik Troan <ewt@redhat.com>
- updated to 1.3

* Tue Oct 28 1997 Cristian Gafton <gafton@redhat.com>
- added BuildRoot; added aclocal files

* Fri Oct 24 1997 Erik Troan <ewt@redhat.com>
- made it a noarch package

* Thu Oct 16 1997 Michael Fulbright <msf@redhat.com>
- Fixed some tag lines to conform to 5.0 guidelines.

* Thu Jul 17 1997 Erik Troan <ewt@redhat.com>
- updated to 1.2

* Wed Mar 5 1997 msf@redhat.com <Michael Fulbright>
- first version (1.0)
