#
# Conditional build:
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
#
%define		_orig_name	adm8211
#
Summary:	Kernel driver for ADM8211 based wireless ethernet cards
Summary(pl):	Sterownik j±dra dla bezprzewodowych kart sieciowych na ADM8211
Name:		kernel-net-%{_orig_name}
Version:	20040601
Release:	1@%{_kernel_ver_str}
License:	GPL
Group:		Base/Kernel
Source0:	http://aluminum.sourmilk.net/%{_orig_name}/%{_orig_name}-%{version}.tar.bz2
#Source0-MD5:	75cd1aea7b79542c8782c873bdba0485
URL:		http://aluminum.sourmilk.net/%{_orig_name}/
%{?with_dist_kernel:BuildRequires:	kernel-module-build >= 2.6.7}
BuildRequires:	%{kgcc_package}
BuildRequires:	rpmbuild(macros) >= 1.153
%{?with_dist_kernel:%requires_releq_kernel_up}
Requires(post,postun):	/sbin/depmod
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Linux kernel driver for ADM8211 based wireless ethernet cards.

%description -l pl
Sterownik j±dra Linuksa dla bezprzewodowych kart sieciowych na ADM8211.

%package -n kernel-smp-net-adm8211
Summary:	SMP kernel driver for ADM8211 based wireless ethernet cards
Summary(pl):	Sterownik j±dra SMP dla bezprzewodowych kart sieciowych na ADM8211
Group:		Base/Kernel
%{?with_dist_kernel:%requires_releq_kernel_smp}
Requires(post,postun):	/sbin/depmod

%description -n kernel-smp-net-adm8211
Linux SMP kernel driver for ADM8211 based wireless ethernet cards.

%description -n kernel-smp-net-adm8211 -l pl
Sterownik j±dra Linuksa SMP dla bezprzewodowych kart sieciowych na
ADM8211.

%prep
%setup -q -n %{_orig_name}

%build
for cfg in %{?with_dist_kernel:%{?with_smp:smp} up}%{!?with_dist_kernel:nondist}; do
    if [ ! -r "%{_kernelsrcdir}/config-$cfg" ]; then
        exit 1
    fi
    rm -rf include
    install -d include/{config,linux}
    ln -sf %{_kernelsrcdir}/config-$cfg .config
    ln -sf %{_kernelsrcdir}/include/linux/autoconf-$cfg.h include/linux/autoconf.h
    ln -sf %{_kernelsrcdir}/include/asm-%{_target_base_arch} include/asm
    touch include/config/MARKER
    %{__make} -C %{_kernelsrcdir} clean modules \
        RCS_FIND_IGNORE="-name '*.ko' -o" \
        M=$PWD O=$PWD \
        %{?with_verbose:V=1}
    mv %{_orig_name}{,-$cfg}.ko
done

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}{,smp}/kernel/drivers/net/wireless
install %{_orig_name}-%{?with_dist_kernel:up}%{!?with_dist_kernel:nondist}.ko \
        $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/%{_orig_name}.ko
%if %{with smp} && %{with dist_kernel}
install %{_orig_name}-smp.ko \
        $RPM_BUILD_ROOT/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/%{_orig_name}.ko
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%depmod %{_kernel_ver}

%postun
%depmod %{_kernel_ver}

%post	-n kernel-smp-net-adm8211
%depmod %{_kernel_ver}smp

%postun -n kernel-smp-net-adm8211
%depmod %{_kernel_ver}smp

%files
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/drivers/net/wireless/*.ko*

%if %{with smp} && %{with dist_kernel}
%files -n kernel-smp-net-adm8211
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/drivers/net/wireless/*.ko*
%endif
