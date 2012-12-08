Summary:	An implementation of the RFC1413 identification server
Name:		pidentd
Version:	3.0.19
Release:	%mkrel 12
License:	GPL
Group:		System/Servers
URL:		http://www.lysator.liu.se/~pen/pidentd/
Source0:	ftp://ftp.lysator.liu.se/pub/unix/ident/servers/%{name}-%{version}.tar.bz2
Source1:	identd.conf
Patch2:		pidentd-3.0.10-install.patch
Patch3:		pidentd-3.0.11-nossl.patch
Patch4:		pidentd-3.0.14-remove_o.patch
Patch5:		pidentd-3.0.19-pinit.patch
Requires(post): rpm-helper
Requires(preun): rpm-helper
Provides:	identd
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The pidentd package contains identd, which implements the RFC1413
identification server. Identd looks up specific TCP/IP connections and returns
either the user name or other information about the process that owns the
connection.

%prep

%setup -q
#%patch0 -p1 -b .dummy
%patch2 -p1 -b .inst
%patch3 -p1
%patch4 -p1
%patch5 -p1 -b .pinit
chmod 644 src/*.{c,h} BUGS ChangeLog FAQ INSTALL README Y2K doc/rfc1413.txt doc/sgi_irix.txt

%build
%serverbuild
autoconf
%configure2_5x --sysconfdir=%{_sysconfdir} --with-threads=yes

%make

%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8

%makeinstall

ln -s identd ${RPM_BUILD_ROOT}%{_sbindir}/in.identd
# dangling symlink (typo ?)
#ln -s identd.8 ${RPM_BUILD_ROOT}%{_sbindir}/in.identd.8
install -m0644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/identd.conf
install -m755 etc/identd.init -D %{buildroot}%{_initrddir}/identd

%post
%_post_service identd

%preun
%_preun_service identd

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc BUGS ChangeLog FAQ INSTALL README Y2K doc/rfc1413.txt doc/sgi_irix.txt
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/identd.conf
%{_initrddir}/identd
%{_mandir}/man8/*


%changelog
* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 3.0.19-12mdv2011.0
+ Revision: 667771
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.19-11mdv2011.0
+ Revision: 607173
- rebuild

* Mon Mar 15 2010 Oden Eriksson <oeriksson@mandriva.com> 3.0.19-10mdv2010.1
+ Revision: 520198
- rebuilt for 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 3.0.19-9mdv2010.0
+ Revision: 426680
- rebuild

* Mon Dec 22 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.19-8mdv2009.1
+ Revision: 317472
- rebuild

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 3.0.19-7mdv2009.0
+ Revision: 224918
- rebuild

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 3.0.19-6mdv2008.1
+ Revision: 179236
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Tue May 29 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.19-5mdv2008.0
+ Revision: 32479
- rebuild

* Tue May 29 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.19-4mdv2008.0
+ Revision: 32476
- fix typo in deps (pm-helper/rpm-helper)


* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.19-4mdv2007.1
+ Revision: 145554
- Import pidentd

* Sat Mar 17 2007 Oden Eriksson <oeriksson@mandriva.com> 3.0.19-4dv2007.1
- use the %%mrel macro
- bunzip patches

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 3.0.19-3mdk
- really include correct parallel init patch

* Mon Jan 09 2006 Olivier Blin <oblin@mandriva.com> 3.0.19-2mdk
- convert parallel init to LSB
- split Requires(X,Y)

* Tue Jan 03 2006 Per Øyvind Karlsen <pkarlsen@mandriva.com> 3.0.19-1mdk
- 3.0.19
- add parallell init
- fix executable-marked-as-config-file
- fix non-readable
- add provides
- %%mkrel

* Sun Jan 01 2006 Mandriva Linux Team <http://www.mandrivaexpert.com/> 3.0.18-2mdk
- Rebuild

* Thu Jan 20 2005 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.0.18-1mdk
- 3.0.18
- drop dummy patch (P0)
- clean up dependencies
- fix summary-ended-with-dot

* Wed Jun 09 2004 Per Øyvind Karlsen <peroyvind@linux-mandrake.com> 3.0.16-3mdk
- fix buildrequires and requires

