#
# spec file for package kernel-obs-build
#
# Copyright (c) 2015 SUSE LINUX Products GmbH, Nuernberg, Germany.
# Copyright (C) 2015 Stefan Seyfried
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# this is extracted from kernel-obs-build.spec of openSUSE kernel rpm

#!BuildIgnore: post-build-checks

Name:           kernel-obs-build
BuildRequires:  coreutils
BuildRequires:  device-mapper
BuildRequires:  util-linux

BuildRequires:  dracut-obs-build
BuildRequires:  kernel
ExclusiveArch:  x86_64
BuildRequires:  dracut
Summary:        package kernel and initrd for OBS VM builds
License:        GPL-2.0
Group:          OBS
Version:        0.42
Release:        0

%description
This package is repackaging already compiled kernels to make them usable
inside of Open Build Service (OBS) VM builds. An initrd with some basic
kernel modules is generated as well, but further kernel modules can be 
loaded during build when installing the kernel package.

%prep

%build
%define kernel_name vmlinu?
mkdir tmp
# a longer list to have them also available for qemu cross builds where x86_64 kernel runs in eg. arm env.
# this list of modules where available on build workers of build.opensuse.org, so we stay compatible.
export KERNEL_MODULES="loop dm-mod dm-snapshot binfmt-misc fuse kqemu squashfs ext2 ext3 ext4 xfs reiserfs btrfs nf_conntrack_ipv6 binfmt_misc virtio_pci virtio_mmio virtio_blk virtio_rng fat vfat nls_cp437 nls_iso8859-1 ibmvscsi ibmvscsic"
KNAME="`echo /boot/%{kernel_name}-* | sed -n -e 's,[^-]*-\(.*\)$,\1,p'`"
dracut -v --host-only --force-add obs --no-early-microcode --drivers="$KERNEL_MODULES" --force tmp/initrd.kvm $KNAME

%install
install -d -m 0755 $RPM_BUILD_ROOT
cp -v /boot/%{kernel_name}-* $RPM_BUILD_ROOT/.build.kernel.kvm
cp -v tmp/initrd.kvm $RPM_BUILD_ROOT/.build.initrd.kvm
#cp -v /boot/%{kernel_name}-* $RPM_BUILD_ROOT/.build.kernel.xen
#cp -v tmp/initrd.xen $RPM_BUILD_ROOT/.build.initrd.xen

#inform worker about arch
#see obs-build commit e47399d738e51
uname -m > $RPM_BUILD_ROOT/.build.hostarch.kvm

%files
%defattr(-,root,root)
/.build.kernel.*
/.build.initrd.*
/.build.hostarch.*

%changelog
