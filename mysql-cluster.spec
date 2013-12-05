%define _build_pkgcheck_set %{nil}
%define _build_pkgcheck_srpm %{nil}

%define Werror_cflags %nil
%define _disable_ld_no_undefined 1

%define _with_systemd 1
#(ie. use with rpm --rebuild):
#
#	--with debug	Compile with debugging code
# 
#  enable build with debugging code: will _not_ strip away any debugging code,
#  will _add_ -g3 to CFLAGS, will _add_ --enable-maintainer-mode to 
#  configure.

%define build_debug 0
%define build_test 0

%if %{build_debug}
# disable build root strip policy
%define __spec_install_post %{_libdir}/rpm/brp-compress || :

# This gives extra debuggin and huge binaries
%{expand:%%define optflags %{optflags} %([ ! $DEBUG ] && echo '-g3')}
%endif

%define _requires_exceptions perl(this)

%define muser	mysql
%define major 18
%define services_major 0
%define services_minor 0.0
%define mysqld_major 0
%define mysqld_minor 0.1

%define libclient %mklibname mysqlclient-cluster %{major}
%define libndbclient %mklibname ndbclient 6
%define libservices %mklibname mysqlservices-cluster %{services_major}
%define libmysqld %mklibname mysqld-cluster %{mysqld_major}
%define devname %mklibname -d mysql-cluster
%define staticname %mklibname -d -s mysql-cluster

Summary:	Version of MySQL with clustering support
Name: 		mysql-cluster
Version:	7.3.3
Release:	1
Group:		Databases
License:	GPLv2
Url:		http://www.mysql.com/
# http://dev.mysql.com/downloads/cluster/
Source0:	http://cdn.mysql.com/Downloads/MySQL-Cluster-%(echo %version |cut -d. -f1-2)/mysql-cluster-gpl-%{version}.tar.gz
#Source1:	%{SOURCE0}.asc
Source2:	mysqld.sysconfig
Source3:	my.cnf
Source4:	libmysql.version
Source5:	mysqld.service
Source6:	mysqld-prepare-db-dir
Source7:	mysqld-wait-ready
# fedora patches
Patch1:		mysql-strmov.patch
Patch2:		mysql-install-test.patch
Patch3:		mysql-expired-certs.patch
Patch5:		mysql-chain-certs.patch
Patch10:	mysql-home.patch
Patch11:	mysqld_safe-nowatch.patch
# mandriva patches
Patch100:	mysql-mysqldumpslow_no_basedir.diff
Patch101:	mysql-logrotate.diff
Patch102:	mysql-initscript.diff
Patch103:	mysql_upgrade-exit-status.patch
Patch104:	mysql-5.1.31-shebang.patch
Patch105:	mysql-5.1.35-test-variables-big.patch
Patch106:	mysql-5.1.36-hotcopy.patch
Patch107:	mysql-install_db-quiet.patch
Patch108:	mysql-5.5.9-INSTALL_INCLUDEDIR_borkfix.diff
Patch109:	mysql-libify_libservices.patch
Patch110:	mysql-5.6.14-mysqld_link.patch
BuildRequires:	bison
BuildRequires:	cmake
BuildRequires:	dos2unix
BuildRequires:	doxygen
BuildRequires:	python
BuildRequires:	systemd-units
BuildRequires:	systemtap
BuildRequires:	libaio-devel
BuildRequires:	stdc++-devel
BuildRequires:	readline-devel
BuildRequires:	xfsprogs-devel
BuildRequires:	pkgconfig(ncursesw)
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  wrap-devel
BuildConflicts:	pkgconfig(libedit)
Requires(post,preun,pre,postun):	rpm-helper
# This basically turns into a metapkg
Requires:	%{name}-server >= %{version}-%{release}
Requires:	%{name}-client >= %{version}-%{release}

%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user, and
robust SQL (Structured Query Language) database server. MySQL Server is
intended for mission-critical, heavy-load production systems as well as for
embedding into mass-deployed software. MySQL is a trademark of MySQL AB.

The mysql server is compiled with the following storage engines:

 - InnoDB Storage Engine
 - Archive Storage Engine
 - CSV Storage Engine
 - Federated Storage Engine
 - User Defined Functions (UDFs).
 - Blackhole Storage Engine
 - Partition Storage Engine
 - Perfschema Storage Engine

%package	server
Summary:	Server mysqld binary
Group:		System/Servers
Conflicts:	mysql < 5.1.39-3
Conflicts:	mysql-max < 5.1.43
# all pkgs needed b/c of cleanup reorg
%rename %{name}-core
%rename %{name}-common-core
Requires:	%{name}-common >= %{version}-%{release}
Requires:	%{name}-plugin >= %{version}-%{release}
Requires(post,preun,pre,postun):	rpm-helper
Obsoletes:	mysql-common < 5.5.25a-1

%description  server
The  mysqld server binary. For a full MySQL database server, install
package 'mysql'.

%package	common
Summary:	Common files
Group:		System/Servers
BuildArch:	noarch
# all pkgs needed b/c of cleanup reorg
Conflicts:	mysql < 5.5.25a-1
Conflicts:	mysql-core < 5.5.25a-1
Obsoletes:	mysql-common-core < 5.5.25a-1

%description	common
Common files for the MySQL(TM) database server.

%package	plugin
Summary:	Mysql Plugins
Group:		Databases
# all pkgs needed b/c of cleanup reorg
Conflicts:	mysql < 5.5.25a-1

%description	plugin
This package contains the standard MySQL plugins.

%package	client
Summary:	Client
Group:		Databases
# all pkgs needed b/c of cleanup reorg
Conflicts:	mysql-core < 5.5.25a-1
Conflicts:	mysql-common < 5.5.25a-1
Conflicts:	mysql-common-core < 5.5.25a-1

%description	client
This package contains the standard MySQL clients.

%package	bench
Summary:	Benchmarks and test system
Group:		System/Servers
Requires:	%{name}-client >= %{version}-%{release}

%description	bench
This package contains MySQL benchmark scripts and data.

%package -n	%{libclient}
Summary:	Shared libraries
Group:		System/Libraries

%description -n	%{libclient}
This package contains the shared %{name}client library.

%package -n	%{libndbclient}
Summary:	NDB (Network DataBase) client library
Group:		System/Libraries

%description -n %{libndbclient}
NDB (Network DataBase) client library

%package -n	%{libservices}
Summary:	Shared %{name}client library
Group:		System/Libraries

%description -n	%{libservices}
The libmysqlservices library provides access to the available services and
dynamic plugins now must be linked against this library 
(use the -lmysqlservices flag).

%package -n	%{libmysqld}
Summary:	Shared libraries
Group:		System/Libraries

%description -n	%{libmysqld}
This package contains the shared %{name}d library so the MySQL server that can
be embedded into a client application instead of running as a separate process.
The API is identical for the embedded MySQL version and the client/server
version.

%package -n	%{devname}
Summary:	Development header files and libraries
Group:		Development/Other
Requires:	%{libclient} = %{version}-%{release}
Requires:	%{libndbclient} = %{EVRD}
Requires:	%{libmysqld} = %{version}-%{release}
Requires:	%{libservices} = %{version}-%{release}
# https://qa.mandriva.com/show_bug.cgi?id=64668
Requires:	rpm-build
Provides:	mysql-devel = %{version}-%{release}

%description -n	%{devname}
This package contains the development header files and libraries necessary to
develop MySQL client applications.

%package -n	%{staticname}
Summary:	Static development libraries
Group:		Development/Other
Requires:	%{devname} >= %{version}-%{release}
Provides:	mysql-static-devel = %{version}-%{release}

%description -n	%{staticname}
This package contains the static development libraries.

%prep
%setup -q -n %{name}-gpl-%{version}

# fedora patches
%patch1 -p1 -b .strmov
%patch2 -p1 -b .install-test
%patch3 -p1 -b .expired-certs
%patch5 -p1 -b .chain-certs
%patch10 -p0 -b .home
%patch11 -p1 -b .nowatch

# mandriva patches
%patch100 -p0 -b .mysqldumpslow_no_basedir
%patch101 -p0 -b .logrotate
%patch102 -p0 -b .initscript
%patch103 -p1 -b .mysql_upgrade-exit-status
%patch104 -p1 -b .shebang
%patch105 -p0 -b .test-variables-big
%patch106 -p0 -b .hotcopy
%patch107 -p0 -b .install_db-quiet
%patch108 -p0 -b .INSTALL_INCLUDEDIR_borkfix
%patch109 -p0 -b .libify_libservices
%patch110 -p1 -b .mysqld_link

mkdir -p Mandriva
cp %{SOURCE2} Mandriva/mysqld.sysconfig
cp %{SOURCE3} Mandriva/my.cnf

# lib64 fix
perl -pi -e "s|/usr/lib/|%{_libdir}/|g" Mandriva/my.cnf

# antiborker
perl -pi -e "s|\@bindir\@|%{_bindir}|g" support-files/* scripts/*
perl -pi -e "s|\@sbindir\@|%{_sbindir}|g" support-files/* scripts/*
perl -pi -e "s|\@libexecdir\@|%{_sbindir}|g" support-files/* scripts/*
perl -pi -e "s|\@localstatedir\@|/var/lib/mysql|g" support-files/* scripts/*
perl -pi -e "s|^basedir=.*|basedir=%{_prefix}|g" support-files/* scripts/mysql_install_db*

# this may be part of the problems with mysql-test
# http://bugs.mysql.com/bug.php?id=52223
#perl -pi -e "s|basedir/lib\b|basedir/%{_lib}\b|g" mysql-test/mysql-test-run.pl
#perl -pi -e "s|basedir/lib/|basedir/%{_lib}/|g" mysql-test/mysql-test-run.pl

# workaround for upstream bug #56342
rm -f mysql-test/t/ssl_8k_key-master.opt

# upstream has fallen down badly on symbol versioning, do it ourselves
cp %{SOURCE4} libmysql/libmysql.version

%build
%serverbuild

# it does not work with -fPIE and someone added that to the serverbuild macro...
CFLAGS=`echo $CFLAGS|sed -e 's|-fPIE||g'`
CXXFLAGS=`echo $CXXFLAGS|sed -e 's|-fPIE||g'`

CFLAGS="$CFLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE"
# MySQL 4.1.10 definitely doesn't work under strict aliasing; also,
# gcc 4.1 breaks MySQL 5.0.16 without -fwrapv
CFLAGS="$CFLAGS -fno-strict-aliasing -fwrapv"
export CFLAGS CXXFLAGS

%cmake \
    -DBUILD_CONFIG=mysql_release \
    -DINSTALL_LAYOUT=RPM \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DCMAKE_INSTALL_PREFIX=%{_prefix} \
    -DINSTALL_SBINDIR=sbin \
    -DMYSQL_DATADIR=/var/lib/mysql \
    -DSYSCONFDIR=%{_sysconfdir} \
    -DINSTALL_PLUGINDIR=%{_lib}/mysql/plugin \
    -DINSTALL_MANDIR=share/man \
    -DINSTALL_SHAREDIR=share/mysql \
    -DINSTALL_LIBDIR=%{_lib} \
    -DINSTALL_INCLUDEDIR=include/mysql \
    -DINSTALL_INFODIR=share/info \
    -DINSTALL_MYSQLDATADIR=/var/lib/mysql \
    -DINSTALL_MYSQLTESTDIR=share/mysql/mysql-test \
    -DINSTALL_SQLBENCHDIR=share/mysql \
    -DINSTALL_SUPPORTFILESDIR=share/mysql \
    -DINSTALL_MYSQLSHAREDIR=share/mysql \
    -DMYSQL_UNIX_ADDR=/var/lib/mysql/mysql.sock \
    -DWITH_READLINE=0 \
    -DWITH_LIBEDIT=0 \
    -DWITH_LIBWRAP=1 \
    -DWITH_SSL=system \
    -DWITH_ZLIB=system \
    -DWITH_PIC=1 \
    -DMYSQL_TCP_PORT=3306 \
    -DEXTRA_CHARSETS=all \
    -DENABLED_LOCAL_INFILE=1 \
    -DENABLE_DTRACE=0 \
    -DWITH_EMBEDDED_SERVER=1 \
    -DMYSQL_USER=%{muser} \
%if %{build_debug}
    -DWITH_DEBUG=1 \
%else
    -DWITH_DEBUG=0 \
%endif
    -DWITHOUT_EXAMPLE_STORAGE_ENGINE=1 \
    -DWITHOUT_NDBCLUSTER_STORAGE_ENGINE=0 \
    -DWITHOUT_DAEMON_EXAMPLE=1 \
    -DFEATURE_SET="community" \
    -DCOMPILATION_COMMENT="%{distribution} - MySQL Community Edition (GPL)" \
    -DLIBSERVICES_SOVERSION="%{services_major}" \
    -DLIBSERVICES_VERSION="%{services_major}.%{services_minor}"

cp ../libmysql/libmysql.version libmysql/libmysql.version

%make
# Upstream bug: http://bugs.mysql.com/68559
mkdir libmysqld/work
pushd libmysqld/work
ar -x ../libmysqld.a
gcc $CFLAGS $LDFLAGS -DEMBEDDED_LIBRARY -shared -Wl,-soname,libmysqld.so.%{mysqld_major} -o libmysqld.so.%{mysqld_major}.%{mysqld_minor} \
	*.o \
	-lpthread -laio -lcrypt -lssl -lcrypto -lz -lrt -lstdc++ -ldl -lm -lc

%install 
# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

%if %{build_debug}
export DONT_STRIP=1
%endif

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_var}/run/mysqld
install -d %{buildroot}%{_var}/log/mysqld
install -d %{buildroot}/var/lib/mysql/{mysql,test}

%makeinstall_std -C build

# install init scripts
install -m0755 build/support-files/mysql.server %{buildroot}%{_initrddir}/mysqld

# install configuration files
install -m0644 Mandriva/mysqld.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/mysqld
install -m0644 Mandriva/my.cnf %{buildroot}%{_sysconfdir}/my.cnf

# bork
mv %{buildroot}%{_bindir}/mysqlaccess.conf %{buildroot}%{_sysconfdir}/
chmod 644 %{buildroot}%{_sysconfdir}/mysqlaccess.conf
mv %{buildroot}%{_datadir}/mysql/aclocal %{buildroot}%{_datadir}/aclocal

pushd %{buildroot}%{_bindir}
    ln -sf mysqlcheck mysqlrepair
    ln -sf mysqlcheck mysqlanalyze
    ln -sf mysqlcheck mysqloptimize
popd

# nuke -Wl,--as-needed from the mysql_config file
perl -pi -e "s|^ldflags=.*|ldflags=\'-rdynamic\'|g" %{buildroot}%{_bindir}/mysql_config

# cmake generates some completely wacko references to -lprobes_mysql when
# building with dtrace support.  Haven't found where to shut that off,
# so resort to this blunt instrument.  While at it, let's not reference
# libmysqlclient_r anymore either.
sed -e 's/-lprobes_mysql//' -e 's/-lmysqlclient_r/-lmysqlclient/' \
	%{buildroot}%{_bindir}/mysql_config >mysql_config.tmp
cp -f mysql_config.tmp %{buildroot}%{_bindir}/mysql_config
chmod 755 %{buildroot}%{_bindir}/mysql_config

# libmysqlclient_r is no more.  Upstream tries to replace it with symlinks
# but that really doesn't work (wrong soname in particular).  We'll keep
# just the devel libmysqlclient_r.so link, so that rebuilding without any
# source change is enough to get rid of dependency on libmysqlclient_r.
rm -f %{buildroot}%{_libdir}/libmysqlclient_r.so*
ln -s libmysqlclient.so %{buildroot}%{_libdir}/libmysqlclient_r.so

# mysql-test includes one executable that doesn't belong under /usr/share,
# so move it and provide a symlink
mv %{buildroot}%{_datadir}/mysql/mysql-test/lib/My/SafeProcess/my_safe_process %{buildroot}%{_bindir}
ln -s %{_bindir}/my_safe_process %{buildroot}%{_datadir}/mysql/mysql-test/lib/My/SafeProcess/my_safe_process

# Remove libmysqld.a, install libmysqld.so
rm -f %{buildroot}%{_libdir}/libmysqld.a
install -m 0755 build/libmysqld/work/libmysqld.so.%{mysqld_major}.%{mysqld_minor} %{buildroot}%{_libdir}/libmysqld.so.%{mysqld_major}.%{mysqld_minor}
ln -s libmysqld.so.%{mysqld_major}.%{mysqld_minor} %{buildroot}%{_libdir}/libmysqld.so.%{mysqld_major}
ln -s libmysqld.so.%{mysqld_major} %{buildroot}%{_libdir}/libmysqld.so

# house cleaning
rm -rf %{buildroot}%{_datadir}/info
rm -f %{buildroot}%{_bindir}/client_test
rm -f %{buildroot}%{_bindir}/make_win_binary_distribution
rm -f %{buildroot}%{_bindir}/make_win_src_distribution
rm -f %{buildroot}%{_datadir}/mysql/binary-configure
rm -f %{buildroot}%{_datadir}/mysql/config.huge.ini
rm -f %{buildroot}%{_datadir}/mysql/config.medium.ini
rm -f %{buildroot}%{_datadir}/mysql/config.small.ini
rm -f %{buildroot}%{_datadir}/mysql/mysqld_multi.server
rm -f %{buildroot}%{_datadir}/mysql/mysql-log-rotate
rm -f %{buildroot}%{_datadir}/mysql/mysql.server
rm -f %{buildroot}%{_datadir}/mysql/binary-configure
rm -f %{buildroot}%{_mandir}/man1/make_win_bin_dist.1*
rm -f %{buildroot}%{_mandir}/man1/make_win_src_distribution.1*
rm -f %{buildroot}%{_datadir}/mysql/magic
rm -f %{buildroot}%{_libdir}/mysql/plugin/daemon_example.ini
rm -f %{buildroot}%{_bindir}/mysql_embedded
rm -rf %{buildroot}%{_datadir}/mysql/solaris

# no idea how to fix this
rm -rf %{buildroot}%{_prefix}/data
rm -rf %{buildroot}%{_prefix}/docs
rm -rf %{buildroot}%{_prefix}/scripts
rm -f %{buildroot}%{_prefix}/COPYING
rm -f %{buildroot}%{_prefix}/INSTALL-BINARY
rm -f %{buildroot}%{_prefix}/README

%multiarch_binaries %{buildroot}%{_bindir}/mysql_config

%multiarch_includes %{buildroot}%{_includedir}/mysql/my_config.h

%if %{_with_systemd}
	# systemd
	mkdir -p %{buildroot}/lib/systemd/system
	install -m644 %{SOURCE5} %{buildroot}%{_systemunitdir}
	install -m 755 %{SOURCE6} %{buildroot}%{_bindir}/
	install -m 755 %{SOURCE7} %{buildroot}%{_bindir}/
%endif
cat > README.urpmi <<EOF

The initscript used to start mysql has been reverted to use the one shipped
by MySQL AB. This means the following changes:

 * The generation of the initial system mysql database is now done when mysql
   is started from the initscript and only if the /var/lib/mysql/mysql
   directory is empty (mysql_install_db). Previousely this was quite hidden and
   silently done at (rpm) install time. As a consequence to this change you may
   have to perform some manual tasks to upgrade the mysql system database and
   such. So, doing something like this might help you:

   /etc/rc.d/init.d/mysqld stop
   TMPDIR=/var/tmp mysql_install_db
   mysql_upgrade

The cluster functionalities (ndb) has been deactivated and will be removed in
future mysql versions. A new product named mysql-cluster has been added (in
contrib) that replaces the cluster functionalities.

The mysql-common-core package ships with a default /etc/my.cnf file that is 
based on the my-medium.cnf file that comes with the source code.

Starting from mysql-5.1.43-2 the storage engines is built as dynamically
loadable modules. You can either load the engines using the /etc/my.cnf file or
at runtime. Please look at these lines in the /etc/my.cnf file to enable
additional engines or disable one or more of the default ones:

plugin_dir=%{_libdir}/mysql/plugin
plugin-load=ha_archive.so;ha_blackhole.so;ha_federated.so

Starting from mysql-5.1.44-3 the html documentation and the mysql.info is not
shipped with the %{distribution} packages due to strict licensing.

EOF

################################################################################
# run the tests
%if %{build_test}
# disable failing tests
echo "rpl_trigger : Unstable test case" >> mysql-test/t/disabled.def
echo "type_enum : Unstable test case" >> mysql-test/t/disabled.def
echo "windows : For MS Windows only" >> mysql-test/t/disabled.def
pushd build/mysql-test
export LANG=C
export LC_ALL=C
export LANGUAGE=C
    perl ./mysql-test-run.pl \
    --mtr-build-thread="$((${RANDOM} % 100))" \
    --skip-ndb \
    --timer \
    --retry=0 \
    --ssl \
    --mysqld=--binlog-format=mixed \
    --testcase-timeout=60 \
    --suite-timeout=120 || false
popd
%endif

%pre server
# delete the mysql group if no mysql user is found, before adding the user
if [ -z "`getent passwd %{muser}`" ] && ! [ -z "`getent group %{muser}`" ]; then
    %{_sbindir}/groupdel %{muser} 2> /dev/null || :
fi

%_pre_useradd %{muser} /var/lib/mysql /bin/bash

%post server
# Change permissions so that the user that will run the MySQL daemon
# owns all needed files.
chown -R %{muser}:%{muser} /var/lib/mysql /var/run/mysqld /var/log/mysqld

# make sure the /var/lib/mysql directory can be accessed
chmod 711 /var/lib/mysql

%_post_service mysqld mysqld.service

%preun server
%_preun_service mysqld mysqld.service

%postun server
%_postun_unit mysqld.service

%pre common
# enable plugins
if [ -f %{_sysconfdir}/my.cnf ]; then
    perl -pi -e "s|^#plugin-load|plugin-load|g" %{_sysconfdir}/my.cnf
    perl -pi -e "s|^#federated|federated|g" %{_sysconfdir}/my.cnf
fi

%triggerun -- %{name} < 5.5.24-1
%_systemd_migrate_service_pre %{name} %{name}d.service

%triggerpostun -- %{name} < 5.5.24-1
%_systemd_migrate_service_post %{name} %{name}d.service

%files
# metapkg

%files plugin
%dir %{_libdir}/mysql/plugin
%{_libdir}/mysql/plugin/adt_null.so
%{_libdir}/mysql/plugin/auth.so
%{_libdir}/mysql/plugin/auth_socket.so
%{_libdir}/mysql/plugin/auth_test_plugin.so
%{_libdir}/mysql/plugin/mypluglib.so
%{_libdir}/mysql/plugin/qa_auth_client.so
%{_libdir}/mysql/plugin/qa_auth_interface.so
%{_libdir}/mysql/plugin/qa_auth_server.so
%{_libdir}/mysql/plugin/semisync_master.so
%{_libdir}/mysql/plugin/semisync_slave.so
%{_libdir}/mysql/plugin/validate_password.so

%files client
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/mysqlaccess.conf
%{_bindir}/msql2mysql
%{_bindir}/mysql
%{_bindir}/mysqlaccess
%{_bindir}/mysqladmin
%{_bindir}/mysqlanalyze
%{_bindir}/mysqlbinlog
%{_bindir}/mysqlcheck
%{_bindir}/mysql_config_editor
%{_bindir}/mysqldump
%{_bindir}/mysqldumpslow
%{_bindir}/mysql_find_rows
%{_bindir}/mysqlimport
%{_bindir}/mysqloptimize
%{_bindir}/mysqlrepair
%{_bindir}/mysqlshow
%{_bindir}/mysqlslap
%{_bindir}/mysql_waitpid
%{_bindir}/my_print_defaults
%{_mandir}/man1/msql2mysql.1*
%{_mandir}/man1/myisam_ftdump.1*
%{_mandir}/man1/mysql.1*
%{_mandir}/man1/mysqlaccess.1*
%{_mandir}/man1/mysqladmin.1*
%{_mandir}/man1/mysqlbinlog.1*
%{_mandir}/man1/mysqlcheck.1*
%{_mandir}/man1/mysqldump.1*
%{_mandir}/man1/mysqldumpslow.1*
%{_mandir}/man1/mysql_find_rows.1*
%{_mandir}/man1/mysqlimport.1*
%{_mandir}/man1/mysqlshow.1*
%{_mandir}/man1/mysql_waitpid.1*
%{_mandir}/man1/my_print_defaults.1*
%{_mandir}/man1/mysql_config_editor.1*
%{_mandir}/man1/ndb*.1*
%{_mandir}/man8/ndb*.8*

%files bench
%doc build/sql-bench/README
%{_bindir}/my_safe_process
%{_bindir}/mysql_client_test
%{_bindir}/mysql_client_test_embedded
%{_bindir}/mysqltest_embedded
%{_datadir}/mysql/sql-bench
%attr(-,mysql,mysql) %{_datadir}/mysql/mysql-test
%{_mandir}/man1/mysql-stress-test.pl.1*
%{_mandir}/man1/mysql-test-run.pl.1*
%{_mandir}/man1/mysql_client_test.1*
%{_mandir}/man1/mysql_client_test_embedded.1*
%{_mandir}/man1/mysqltest.1*
%{_mandir}/man1/mysqltest_embedded.1*

%files server
%doc README.urpmi
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/mysqld
%{_initrddir}/mysqld
%{_bindir}/innochecksum
%{_bindir}/myisamchk
%{_bindir}/myisam_ftdump
%{_bindir}/myisamlog
%{_bindir}/myisampack
%{_bindir}/mysql_convert_table_format
%{_bindir}/mysql_fix_extensions 
%{_bindir}/mysqlbug
%{_bindir}/mysqld_multi
%{_bindir}/mysqld_safe
%{_bindir}/mysqlhotcopy
%{_bindir}/mysql_install_db
%{_bindir}/mysql_plugin
%{_bindir}/mysql_secure_installation
%{_bindir}/mysql_setpermission
%{_bindir}/mysqltest
%{_bindir}/mysql_tzinfo_to_sql
%{_bindir}/mysql_upgrade
%{_bindir}/mysql_zap
%{_bindir}/perror
%{_bindir}/replace
%{_bindir}/resolveip
%{_bindir}/resolve_stack_dump
%{_sbindir}/mysqld
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql/mysql
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql/test
%attr(0755,%{muser},%{muser}) %dir %{_var}/run/mysqld
%attr(0755,%{muser},%{muser}) %dir %{_var}/log/mysqld
%{_datadir}/mysql/*.cnf
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/errmsg-utf8.txt
%{_datadir}/mysql/dictionary.txt
%{_datadir}/mysql/mysql_security_commands.sql
%{_datadir}/mysql/innodb_memcached_config.sql
%{_mandir}/man1/innochecksum.1*
%{_mandir}/man1/myisamchk.1*
%{_mandir}/man1/myisamlog.1*
%{_mandir}/man1/myisampack.1*
%{_mandir}/man1/mysqlbug.1*
%{_mandir}/man1/mysql_convert_table_format.1*
%{_mandir}/man1/mysqld_multi.1*
%{_mandir}/man1/mysqld_safe.1*
%{_mandir}/man1/mysql_fix_extensions.1*
%{_mandir}/man1/mysqlhotcopy.1*
%{_mandir}/man1/mysql_install_db.1*
%{_mandir}/man1/mysqlman.1*
%{_mandir}/man1/mysql_plugin.1*
%{_mandir}/man1/mysql_secure_installation.1*
%{_mandir}/man1/mysql.server.1*
%{_mandir}/man1/mysql_setpermission.1*
%{_mandir}/man1/mysqlslap.1*
%{_mandir}/man1/mysql_tzinfo_to_sql.1*
%{_mandir}/man1/mysql_upgrade.1*
%{_mandir}/man1/mysql_zap.1*
%{_mandir}/man1/perror.1*
%{_mandir}/man1/replace.1*
%{_mandir}/man1/resolveip.1*
%{_mandir}/man1/resolve_stack_dump.1*
%{_mandir}/man8/mysqld.8*

%{_systemunitdir}/mysqld.service
%{_bindir}/mysqld-prepare-db-dir
%{_bindir}/mysqld-wait-ready

# ndb/cluster specific bits
%{_bindir}/mcc_config.py
%{_bindir}/memclient
%{_bindir}/ndb*
%{_datadir}/mysql/mcc
%{_datadir}/mysql/memcache-api
%{_datadir}/mysql/ndb_dist_priv.sql
%{_datadir}/mysql/nodejs
%{_libdir}/ndb_engine.so
%{_sbindir}/memcached
%{_sbindir}/ndb_mgmd
%{_sbindir}/ndbd
%{_sbindir}/ndbmtd
%{_datadir}/mysql/java/clusterj*.jar

%files common
%doc README COPYING
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/my.cnf
%dir %{_datadir}/mysql
%{_datadir}/mysql/english
%{_datadir}/mysql/bulgarian
%{_datadir}/mysql/charsets
%{_datadir}/mysql/czech
%{_datadir}/mysql/danish
%{_datadir}/mysql/dutch
%{_datadir}/mysql/estonian
%{_datadir}/mysql/french
%{_datadir}/mysql/german
%{_datadir}/mysql/greek
%{_datadir}/mysql/hungarian
%{_datadir}/mysql/italian
%{_datadir}/mysql/japanese
%{_datadir}/mysql/korean
%{_datadir}/mysql/norwegian
%{_datadir}/mysql/norwegian-ny
%{_datadir}/mysql/polish
%{_datadir}/mysql/portuguese
%{_datadir}/mysql/romanian
%{_datadir}/mysql/russian
%{_datadir}/mysql/serbian
%{_datadir}/mysql/slovak
%{_datadir}/mysql/spanish
%{_datadir}/mysql/swedish
%{_datadir}/mysql/ukrainian

%files -n %{libclient}
%{_libdir}/libmysqlclient.so.%{major}*

%files -n %{libndbclient}
%{_libdir}/libndbclient.so.6*

%files -n %{libservices}
%{_libdir}/libmysqlservices.so.%{services_major}*

%files -n %{libmysqld}
%{_libdir}/libmysqld.so.%{mysqld_major}*

%files -n %{devname}
%doc INSTALL-SOURCE
%doc Docs/ChangeLog
%{multiarch_bindir}/mysql_config
%{_bindir}/mysql_config
%{_libdir}/libmysqlclient_r.so
%{_libdir}/libmysqlclient.so
%{_libdir}/libmysqlservices.so
%{_libdir}/libmysqld.so
%dir %{_includedir}/mysql
%dir %{_includedir}/mysql/psi
%{_includedir}/mysql/*.h
%{_includedir}/mysql/*.h.pp
%{_includedir}/mysql/psi/*.h
%{multiarch_includedir}/mysql/my_config.h
%{_mandir}/man1/comp_err.1*
%{_mandir}/man1/mysql_config.1*
%{_datadir}/aclocal/mysql.m4

# ndb/cluster specific bits
%dir %{_includedir}/mysql/storage
%{_includedir}/mysql/storage/ndb
%{_libdir}/libndbclient.so

%files -n %{staticname}
%{_libdir}/*.a

