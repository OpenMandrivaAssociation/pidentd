Summary:	An implementation of the RFC1413 identification server
Name:		pidentd
Version:	3.0.19
Release:	%mkrel 8
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
