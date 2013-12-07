Summary:	An implementation of the RFC1413 identification server
Name:		pidentd
Version:	3.0.19
Release:	15
License:	GPLv2
Group:		System/Servers
Url:		http://www.lysator.liu.se/~pen/pidentd/
Source0:	ftp://ftp.lysator.liu.se/pub/unix/ident/servers/%{name}-%{version}.tar.gz
Source1:	identd.conf
Patch2:		pidentd-3.0.10-install.patch
Patch3:		pidentd-3.0.11-nossl.patch
Patch4:		pidentd-3.0.14-remove_o.patch
Patch5:		pidentd-3.0.19-pinit.patch
Requires(post,preun):	rpm-helper
Provides:	identd

%description
The pidentd package contains identd, which implements the RFC1413
identification server. Identd looks up specific TCP/IP connections and returns
either the user name or other information about the process that owns the
connection.

%prep
%setup -q
%apply_patches
chmod 644 src/*.{c,h} BUGS ChangeLog FAQ INSTALL README Y2K doc/rfc1413.txt doc/sgi_irix.txt
autoconf

%build
%serverbuild
%configure2_5x \
	--sysconfdir=%{_sysconfdir} \
	--with-threads=yes

%make

%install
mkdir -p %{buildroot}%{_sbindir}
mkdir -p %{buildroot}%{_mandir}/man8

%makeinstall

ln -s identd %{buildroot}%{_sbindir}/in.identd
# dangling symlink (typo ?)
#ln -s identd.8 ${RPM_BUILD_ROOT}%{_sbindir}/in.identd.8
install -m0644 %{SOURCE1} -D %{buildroot}%{_sysconfdir}/identd.conf
install -m755 etc/identd.init -D %{buildroot}%{_initrddir}/identd

%post
%_post_service identd

%preun
%_preun_service identd

%files
%doc BUGS ChangeLog FAQ INSTALL README Y2K doc/rfc1413.txt doc/sgi_irix.txt
%{_sbindir}/*
%config(noreplace) %{_sysconfdir}/identd.conf
%{_initrddir}/identd
%{_mandir}/man8/*

