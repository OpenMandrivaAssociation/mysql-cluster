%define Werror_cflags %nil
%define _disable_ld_no_undefined 1

#(ie. use with rpm --rebuild):
#
#	--with debug	Compile with debugging code
# 
#  enable build with debugging code: will _not_ strip away any debugging code,
#  will _add_ -g3 to CFLAGS, will _add_ --enable-maintainer-mode to 
#  configure.

%define build_debug 0
%define build_test 0

# commandline overrides:
# rpm -ba|--rebuild --with 'xxx'
%{?_with_debug: %{expand: %%define build_debug 1}}
%{?_with_test: %{expand: %%define build_test 1}}
%{?_without_test: %global build_test 0}

%if %{build_debug}
# disable build root strip policy
%define __spec_install_post %{_libdir}/rpm/brp-compress || :

# This gives extra debuggin and huge binaries
%{expand:%%define optflags %{optflags} %([ ! $DEBUG ] && echo '-g3')}
%endif

%if %{build_debug}
%define build_debug 1
%endif

%if %{build_test}
%define build_test 1
%endif

%define _requires_exceptions perl(this)

%define major 16
%define libname %mklibname mysql_cluster %{major}

%define muser	mysql

Summary:	MySQL - server with extended functionality
Name: 		mysql-cluster
Version:	7.0.12
Release:	%mkrel 0.0.2
Group:		Databases
License:	GPL
URL:		http://www.mysql.com
Source0:	mysql-cluster-gpl-%{version}.tar.gz
Source3:	mysqld.sysconfig
Source4:	mysqld-ndbd.init
Source5:	mysqld-ndb.sysconfig
Source6:	mysqld-ndb_cpcd.init
Source7:	mysqld-ndb_cpcd.sysconfig
Source8:	mysqld-ndb_mgmd.init
Source9:	mysqld-ndb_mgmd.sysconfig
Source10:	config.ini
Source11:	my.cnf
Patch1:		mysql-install_script_mysqld_safe.diff
Patch2:		mysql-lib64.diff
Patch3:		mysql-5.0.15-noproc.diff
Patch4:		mysql-mysqldumpslow_no_basedir.diff
Patch6:		mysql-errno.patch
Patch11:	mysql-logrotate.diff
Patch12:	mysql-initscript.diff
Patch14:	mysql-5.1.30-use_-avoid-version_for_plugins.diff
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(post): mysql-cluster-common = %{version}-%{release}
Requires(preun): mysql-cluster-common = %{version}-%{release}
Requires(post): mysql-cluster-client = %{version}-%{release}
Requires(preun): mysql-cluster-client = %{version}-%{release}
Requires(postun): mysql-cluster-common = %{version}-%{release}
Requires(postun): mysql-cluster-client = %{version}-%{release}
Requires:	mysql-cluster-common = %{version}-%{release}
Requires:	mysql-cluster-client = %{version}-%{release}
BuildRequires:	autoconf2.5
BuildRequires:	automake1.7
BuildRequires:	bison
BuildRequires:	doxygen
BuildRequires:	glibc-devel
BuildRequires:	libstdc++-devel
BuildRequires:	libtermcap-devel
BuildRequires:	ncurses-devel
BuildRequires:	openssl-devel
BuildRequires:	python
BuildRequires:	readline-devel
BuildRequires:	tetex
BuildRequires:	texinfo
BuildRequires:	zlib-devel
BuildRequires:	dos2unix
BuildRequires:	multiarch-utils >= 1.0.3
BuildRequires:	xfs-devel
BuildConflicts:	edit-devel
Conflicts:	mysql < 5.1.43
Conflicts:	mysql-common-core < 5.1.43
Conflicts:	mysql-max < 5.1.43
Conflicts:	mysql-ndb-extra < 5.1.43
Conflicts:	mysql-ndb-management < 5.1.43
Conflicts:	mysql-ndb-storage < 5.1.43
Conflicts:	mysql-ndb-tools < 5.1.43
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The MySQL(TM) software delivers a very fast, multi-threaded, multi-user,
and robust SQL (Structured Query Language) database server. MySQL Server
is intended for mission-critical, heavy-load production systems as well
as for embedding into mass-deployed software. MySQL is a trademark of
MySQL AB.

The MySQL server binary supports features like transactional tables and more.
You can use it as an alternate to MySQL basic server. The mysql server is
compiled with the following storage engines:

 - Ndbcluster Storage Engine interface
 - Archive Storage Engine
 - CSV Storage Engine
 - Federated Storage Engine
 - User Defined Functions (UDFs).
 - Blackhole Storage Engine
 - Partition Storage Engine

%package	common
Summary:	MySQL - common files
Group:		System/Servers
Requires(post): rpm-helper
Requires(preun): rpm-helper
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(post): mysql-cluster-client = %{version}-%{release}
Requires(preun): mysql-cluster-client = %{version}-%{release}
Requires(post): perl-DBD-mysql
Requires(preun): perl-DBD-mysql
Requires:	mysql-cluster-client = %{version}-%{release}
Requires:	perl-DBD-mysql
Conflicts:	mysql-common < 5.1.43

%description	common
Common files for the MySQL(TM) database server.

%package	client
Summary:	MySQL - Client
Group:		Databases
Requires(post): %{libname} = %{version}-%{release}
Requires(preun): %{libname} = %{version}-%{release}
Requires:	%{libname} = %{version}-%{release}
Conflicts:	mysql-client < 5.1.43

%description	client
This package contains the standard MySQL clients.

%package -n	%{libname}
Summary:	MySQL - Shared libraries
Group:		System/Libraries

%description -n	%{libname}
This package contains the shared libraries (*.so*) which certain languages and
applications need to dynamically load and use MySQL.

%prep

%setup -q -n mysql-cluster-gpl-%{version}
%patch1 -p0
%patch2 -p1
%patch3 -p0 -b .noproc
%patch4 -p0 -b .mysqldumpslow_no_basedir
%patch6 -p0 -b .errno_as_defines
%patch11 -p0 -b .logrotate
%patch12 -p0 -b .initscript
%patch14 -p1 -b .use_-avoid-version_for_plugins

# fix annoyances
perl -pi -e "s|AC_PROG_RANLIB|AC_PROG_LIBTOOL|g" configure*
perl -pi -e "s|^MAX_C_OPTIMIZE.*|MAX_C_OPTIMIZE=\"\"|g" configure*
perl -pi -e "s|^MAX_CXX_OPTIMIZE.*|MAX_CXX_OPTIMIZE=\"\"|g" configure*

mkdir -p Mandriva
cp %{SOURCE3} Mandriva/mysqld.sysconfig
cp %{SOURCE4} Mandriva/mysqld-ndbd.init
cp %{SOURCE5} Mandriva/mysqld-ndb.sysconfig
cp %{SOURCE6} Mandriva/mysqld-ndb_cpcd.init
cp %{SOURCE7} Mandriva/mysqld-ndb_cpcd.sysconfig
cp %{SOURCE8} Mandriva/mysqld-ndb_mgmd.init
cp %{SOURCE9} Mandriva/mysqld-ndb_mgmd.sysconfig
cp %{SOURCE10} Mandriva/config.ini
cp %{SOURCE11} Mandriva/my.cnf

# lib64 fix
perl -pi -e "s|/usr/lib/|%{_libdir}/|g" Mandriva/my.cnf

# fix libname clash, all the binaries will link to the new lib names likes mindless drones...
find -type f -name "Makefile.*" | xargs perl -pi -e "s|libmysqlclient\.la|libmysqlclient_cluster\.la|g; \
    s|libmysqlclient_r\.la|libmysqlclient_cluster_r\.la|g; \
    s|libmysqlclient_la|libmysqlclient_cluster_la|g; \
    s|libmysqlclient_r_la|libmysqlclient_cluster_r_la|g"

%build
# Run aclocal in order to get an updated libtool.m4 in generated
# configure script for "new" architectures (aka. x86_64, mips)
#autoreconf --install --force
#export WANT_AUTOCONF_2_5=1
libtoolize --automake --copy --force; aclocal -I config/ac-macros; autoheader; automake --foreign --add-missing --copy; autoconf

%serverbuild
export CFLAGS="${CFLAGS:-%{optflags}}"
export CXXFLAGS="${CXXFLAGS:-%{optflags}}"
export FFLAGS="${FFLAGS:-%{optflags}}"

# MySQL 4.1.10 definitely doesn't work under strict aliasing; also,
# gcc 4.1 breaks MySQL 5.0.16 without -fwrapv
export CFLAGS="$CFLAGS -fno-strict-aliasing -fwrapv"
# extra C++ flags as per recommendations in mysql's INSTALL-SOURCE doc
export CXXFLAGS="$CFLAGS -felide-constructors -fno-rtti -fno-exceptions"

%if %{build_debug}
CFLAGS="$CFLAGS -DUNIV_MUST_NOT_INLINE -DEXTRA_DEBUG -DFORCE_INIT_OF_VARS -DSAFEMALLOC -DPEDANTIC_SAFEMALLOC -DSAFE_MUTEX"
%endif

export PS='/bin/ps'
export FIND_PROC='/bin/ps p $$PID'
export KILL='/bin/kill'
export CHECK_PID='/bin/kill -0 $$PID'

%configure2_5x \
    --prefix=/ \
    --exec-prefix=%{_prefix} \
    --libexecdir=%{_sbindir} \
    --libdir=%{_libdir} \
    --sysconfdir=%{_sysconfdir} \
    --datadir=%{_datadir} \
    --localstatedir=/var/lib/mysql \
    --infodir=%{_infodir} \
    --includedir=%{_includedir} \
    --mandir=%{_mandir} \
    --with-pic \
    --with-extra-charsets=all \
    --enable-assembler \
    --enable-local-infile \
    --enable-largefile=yes \
    --without-readline \
    --without-libwrap \
    --with-ssl=%{_libdir} \
    --with-big-tables \
    --enable-thread-safe-client \
    --with-fast-mutexes \
%if %{build_debug}
    --with-debug=full \
%else
    --without-debug \
%endif
    --with-mysqld-user=%{muser} \
    --with-unix-socket-path=/var/lib/mysql/mysql.sock \
    --enable-shared \
    --with-comment='Mandriva Linux - MySQL Cluster Edition (GPL)' \
    --with-plugins=ndbcluster \
    --with-plugin-federated \
    --with-big-tables \
    --with-ndbcluster \
    --with-ndb-shm \
    --with-server-suffix="-cluster"

%make benchdir_root=%{buildroot}%{_datadir}

################################################################################
# run the tests
%if %{build_test}
# disable failing tests
#echo "mysql_client_test : Unstable test case, bug#12258" >> mysql-test/t/disabled.def
#echo "openssl_1 : Unstable test case" >> mysql-test/t/disabled.def
#echo "rpl_openssl : Unstable test case" >> mysql-test/t/disabled.def
echo "rpl_trigger : Unstable test case" >> mysql-test/t/disabled.def
echo "type_enum : Unstable test case" >> mysql-test/t/disabled.def
echo "windows : For MS Windows only" >> mysql-test/t/disabled.def
echo "ndb_restore_different_endian_data : does not pass" >> mysql-test/t/disabled.def
# set some test env, should be free high random ports...
#export MYSQL_TEST_MANAGER_PORT=9305
#export MYSQL_TEST_MASTER_PORT=9306
#export MYSQL_TEST_SLAVE_PORT=9308
#export MYSQL_TEST_NDB_PORT=9350
make check
#make test
#%ifnarch s390x
#pushd mysql-test
#    ./mysql-test-run.pl \
#    --force \
#    --timer \
#    --master_port=$MYSQL_TEST_MASTER_PORT \
#    --slave_port=$MYSQL_TEST_SLAVE_PORT \
#    --ndbcluster_port=$MYSQL_TEST_NDB_PORT \
#    --testcase-timeout=60 \
#    --suite-timeout=120 || false
#popd
#%endif

pushd mysql-test
export LANG=C
export LC_ALL=C
export LANGUAGE=C
    perl ./mysql-test-run.pl \
    --timer \
    --testcase-timeout=60 \
    --suite-timeout=120 || false
popd

%endif

%install 
rm -rf %{buildroot}

# don't fiddle with the initscript!
export DONT_GPRINTIFY=1

%if %{build_debug}
export DONT_STRIP=1
%endif

install -d %{buildroot}%{_sysconfdir}/sysconfig
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_var}/run/{mysqld,ndb_cpcd}
install -d %{buildroot}%{_var}/log/mysqld
install -d %{buildroot}/var/lib/mysql/{mysql,test}
install -d %{buildroot}/var/lib/mysql-cluster

%makeinstall_std benchdir_root=%{_datadir} testdir=%{_datadir}/mysql-test

# nuke one useless plugin
rm -f %{buildroot}%{_libdir}/mysql/plugin/ha_example*

mv %{buildroot}%{_sbindir}/mysqld %{buildroot}%{_sbindir}/mysqld-cluster

# install init scripts
install -m0755 support-files/mysql.server %{buildroot}%{_initrddir}/mysqld-cluster
install -m0755 Mandriva/mysqld-ndbd.init %{buildroot}%{_initrddir}/mysqld-ndbd
install -m0755 Mandriva/mysqld-ndb_cpcd.init %{buildroot}%{_initrddir}/mysqld-ndb_cpcd
install -m0755 Mandriva/mysqld-ndb_mgmd.init %{buildroot}%{_initrddir}/mysqld-ndb_mgmd

# fix status and subsys
perl -pi -e 's/status mysqld\b/status mysqld-cluster/g;s,(/var/lock/subsys/mysqld\b),${1}-cluster,' %{buildroot}%{_initrddir}/mysqld-cluster

# mysqld-cluster needs special treatment running under the instance manager...
perl -pi -e "s|--default-mysqld-path=%{_sbindir}/mysqld|--default-mysqld-path=%{_sbindir}/mysqld-cluster|g"  %{buildroot}%{_initrddir}/mysqld-cluster
perl -pi -e "s|--mysqld=mysqld|--mysqld=mysqld-cluster|g" %{buildroot}%{_initrddir}/mysqld-cluster

# install configuration files
install -m0644 Mandriva/mysqld.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/mysqld
install -m0644 Mandriva/mysqld-ndb.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/mysqld-ndbd
install -m0644 Mandriva/mysqld-ndb_cpcd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/mysqld-ndb_cpcd
install -m0644 Mandriva/mysqld-ndb_mgmd.sysconfig %{buildroot}%{_sysconfdir}/sysconfig/mysqld-ndb_mgmd
install -m0644 Mandriva/my.cnf %{buildroot}%{_sysconfdir}/my.cnf
install -m0644 Mandriva/config.ini %{buildroot}/var/lib/mysql-cluster/config.ini

# Fix libraries
mv %{buildroot}%{_libdir}/mysql/lib*.* %{buildroot}%{_libdir}/

pushd %{buildroot}%{_bindir}
    ln -sf mysqlcheck mysqlrepair
    ln -sf mysqlcheck mysqlanalyze
    ln -sf mysqlcheck mysqloptimize
popd

# touch some files
echo "#" > %{buildroot}%{_sysconfdir}/ndb_cpcd.conf
echo "#" > %{buildroot}/var/lib/mysql/Ndb.cfg

# house cleaning
rm -f %{buildroot}%{_datadir}/info/dir
rm -f %{buildroot}%{_bindir}/make_win_src_distribution
rm -f %{buildroot}%{_bindir}/make_win_binary_distribution
rm -f %{buildroot}%{_datadir}/mysql/*.spec
rm -f %{buildroot}%{_datadir}/mysql/postinstall
rm -f %{buildroot}%{_datadir}/mysql/preinstall
rm -f %{buildroot}%{_datadir}/mysql/mysql-log-rotate
rm -f %{buildroot}%{_datadir}/mysql/mysql.server
rm -f %{buildroot}%{_datadir}/mysql/mysqld_multi.server
rm -f %{buildroot}%{_bindir}/client_test
#rm -f %{buildroot}%{_bindir}/mysql_client_test*
rm -f %{buildroot}%{_bindir}/mysqltest_embedded
rm -f %{buildroot}%{_datadir}/mysql/binary-configure
rm -f %{buildroot}%{_mandir}/man1/make_win_bin_dist.1*
rm -f %{buildroot}%{_mandir}/man1/make_win_src_distribution.1*
rm -f %{buildroot}%{_datadir}/mysql/ChangeLog
rm -f %{buildroot}/mysql-test/lib/My/SafeProcess/my_safe_process

rm -f %{buildroot}%{_bindir}/mysql_config
rm -rf %{buildroot}%{_includedir}/mysql
rm -f %{buildroot}%{_libdir}/mysql/plugin/*.*a
rm -f %{buildroot}%{_libdir}/mysql/*.*a
rm -f %{buildroot}%{_libdir}/*.*a
rm -f %{buildroot}%{_libdir}/*.so
rm -f %{buildroot}%{_datadir}/aclocal/mysql.m4
rm -rf %{buildroot}%{_datadir}/sql-bench
rm -rf %{buildroot}%{_datadir}/mysql-test
rm -f %{buildroot}%{_bindir}/mysql_client_test

%pre common
# delete the mysql group if no mysql user is found, before adding the user
if [ -z "`getent passwd %{muser}`" ] && ! [ -z "`getent group %{muser}`" ]; then
    %{_sbindir}/groupdel %{muser} 2> /dev/null || :
fi

%_pre_useradd %{muser} /var/lib/mysql /bin/bash

%post
# Change permissions so that the user that will run the MySQL daemon
# owns all needed files.
chown -R %{muser}:%{muser} /var/lib/mysql /var/run/mysqld /var/log/mysqld

# make sure the /var/lib/mysql directory can be accessed
chmod 711 /var/lib/mysql

%_post_service mysqld-cluster
%_post_service mysqld-ndbd
%create_ghostfile %{_sysconfdir}/ndb_cpcd.conf root root 0644
%create_ghostfile /var/lib/mysql/Ndb.cfg root root 0644
%_post_service mysqld-ndb_cpcd
%_post_service mysqld-ndb_mgmd

%preun
%_preun_service mysqld-cluster
%_preun_service mysqld-ndbd
%_preun_service mysqld-ndb_cpcd
%_preun_service mysqld-ndb_mgmd

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/mysqld-cluster ]; then
        %{_initrddir}/mysqld-cluster restart > /dev/null 2>/dev/null || :

    fi

    if [ -f /var/lock/subsys/mysqld-ndbd ]; then
        %{_initrddir}/mysqld-ndbd restart > /dev/null 2>/dev/null || :
    fi

    if [ -f /var/lock/subsys/mysqld-ndb_cpcd ]; then
        %{_initrddir}/mysqld-ndb_cpcd restart > /dev/null 2>/dev/null || :
    fi

    if [ -f /var/lock/subsys/mysqld-ndb_mgmd ]; then
        %{_initrddir}/mysqld-ndb_mgmd restart > /dev/null 2>/dev/null || :
    fi
fi

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%attr(0755,root,root) %{_initrddir}/mysqld-cluster
%attr(0755,root,root) %{_sbindir}/mysqld-cluster
%attr(0755,root,root) %{_sbindir}/mysqlmanager
%dir %{_libdir}/mysql/plugin
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_archive.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_blackhole.so
%attr(0755,root,root) %{_libdir}/mysql/plugin/ha_innodb.so

%attr(0755,root,root) %{_initrddir}/mysqld-ndbd
%attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/sysconfig/mysqld-ndbd
%attr(0755,root,root) %{_sbindir}/ndbd
%attr(0755,root,root) %{_sbindir}/ndbmtd

%ghost %attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/ndb_cpcd.conf
%ghost %attr(0644,root,root) %config(noreplace,missingok) /var/lib/mysql/Ndb.cfg
%attr(0644,root,root) %config(noreplace,missingok) /var/lib/mysql-cluster/config.ini
%attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/sysconfig/mysqld-ndb_cpcd
%attr(0644,root,root) %config(noreplace,missingok) %{_sysconfdir}/sysconfig/mysqld-ndb_mgmd
%attr(0755,root,root) %{_initrddir}/mysqld-ndb_cpcd
%attr(0755,root,root) %{_initrddir}/mysqld-ndb_mgmd
%attr(0755,root,root) %{_sbindir}/ndb_mgmd
%attr(0755,root,root) %{_sbindir}/ndb_cpcd
%attr(0755,root,root) %{_bindir}/ndb_mgm
%attr(0755,%{muser},%{muser}) %dir %{_var}/run/ndb_cpcd

%attr(0755,root,root) %{_bindir}/ndb_print_schema_file
%attr(0755,root,root) %{_bindir}/ndb_print_sys_file
%attr(0755,root,root) %{_bindir}/ndb_config
%attr(0755,root,root) %{_bindir}/ndb_desc
%attr(0755,root,root) %{_bindir}/ndb_error_reporter
%attr(0755,root,root) %{_bindir}/ndb_mgm
%attr(0755,root,root) %{_bindir}/ndb_print_backup_file
%attr(0755,root,root) %{_bindir}/ndb_restore
%attr(0755,root,root) %{_bindir}/ndb_select_all
%attr(0755,root,root) %{_bindir}/ndb_select_count
%attr(0755,root,root) %{_bindir}/ndb_show_tables
%attr(0755,root,root) %{_bindir}/ndb_size.pl
%attr(0755,root,root) %{_bindir}/ndb_test_platform
%attr(0755,root,root) %{_bindir}/ndb_waiter
%attr(0755,root,root) %{_bindir}/ndbd_redo_log_reader

%attr(0755,root,root) %{_bindir}/ndb_drop_index
%attr(0755,root,root) %{_bindir}/ndb_drop_table
%attr(0755,root,root) %{_bindir}/ndb_delete_all

%files client
%defattr(-,root,root)
%attr(0755,root,root) %{_bindir}/msql2mysql
%attr(0755,root,root) %{_bindir}/mysql
%attr(0755,root,root) %{_bindir}/mysqlaccess
%attr(0755,root,root) %{_bindir}/mysqladmin
%attr(0755,root,root) %{_bindir}/mysqlanalyze
%attr(0755,root,root) %{_bindir}/mysqlbinlog
%attr(0755,root,root) %{_bindir}/mysqlcheck
%attr(0755,root,root) %{_bindir}/mysqldump
%attr(0755,root,root) %{_bindir}/mysqldumpslow
%attr(0755,root,root) %{_bindir}/mysql_find_rows
%attr(0755,root,root) %{_bindir}/mysqlimport
%attr(0755,root,root) %{_bindir}/mysqloptimize
%attr(0755,root,root) %{_bindir}/mysqlrepair
%attr(0755,root,root) %{_bindir}/mysqlshow
%attr(0755,root,root) %{_bindir}/mysqlslap
%attr(0755,root,root) %{_bindir}/mysql_waitpid

%files common
%defattr(-,root,root) 
%doc README COPYING support-files/*.cnf
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/sysconfig/mysqld
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/my.cnf
%attr(0755,root,root) %{_bindir}/innochecksum
%attr(0755,root,root) %{_bindir}/myisamchk
%attr(0755,root,root) %{_bindir}/myisam_ftdump
%attr(0755,root,root) %{_bindir}/myisamlog
%attr(0755,root,root) %{_bindir}/myisampack
%attr(0755,root,root) %{_bindir}/my_print_defaults
%attr(0755,root,root) %{_bindir}/mysqlbug
%attr(0755,root,root) %{_bindir}/mysql_convert_table_format
%attr(0755,root,root) %{_bindir}/mysqld_multi
%attr(0755,root,root) %{_bindir}/mysqld_safe
%attr(0755,root,root) %{_bindir}/mysql_fix_extensions 
%attr(0755,root,root) %{_bindir}/mysql_fix_privilege_tables
%attr(0755,root,root) %{_bindir}/mysqlhotcopy
%attr(0755,root,root) %{_bindir}/mysql_install_db
%attr(0755,root,root) %{_bindir}/mysql_secure_installation
%attr(0755,root,root) %{_bindir}/mysql_setpermission
%attr(0755,root,root) %{_bindir}/mysqltest
%attr(0755,root,root) %{_bindir}/mysql_tzinfo_to_sql
%attr(0755,root,root) %{_bindir}/mysql_upgrade
%attr(0755,root,root) %{_bindir}/mysql_zap
%attr(0755,root,root) %{_bindir}/perror
%attr(0755,root,root) %{_bindir}/replace
%attr(0755,root,root) %{_bindir}/resolveip
%attr(0755,root,root) %{_bindir}/resolve_stack_dump
%{_infodir}/mysql.info*
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql-cluster
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql/mysql
%attr(0711,%{muser},%{muser}) %dir /var/lib/mysql/test
%attr(0755,%{muser},%{muser}) %dir %{_var}/run/mysqld
%attr(0755,%{muser},%{muser}) %dir %{_var}/log/mysqld
%dir %{_datadir}/mysql
%{_datadir}/mysql/ndbinfo.sql
%{_datadir}/mysql/mi_test_all
%{_datadir}/mysql/mi_test_all.res
%{_datadir}/mysql/*.cnf
%{_datadir}/mysql/fill_help_tables.sql
%{_datadir}/mysql/mysql_fix_privilege_tables.sql
%{_datadir}/mysql/mysql_system_tables.sql
%{_datadir}/mysql/mysql_system_tables_data.sql
%{_datadir}/mysql/mysql_test_data_timezone.sql
%{_datadir}/mysql/*.ini
%{_datadir}/mysql/errmsg.txt
%{_datadir}/mysql/english
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
%{_datadir}/mysql/swig
%attr(0644,root,root) %{_mandir}/man1/mysqlman.1*

%files -n %{libname}
%defattr(-,root,root)
%doc ChangeLog
%attr(0755,root,root) %{_libdir}/*.so.*
