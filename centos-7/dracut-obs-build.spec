#
# spec file for package dracut-obs-build
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

Name:           dracut-obs-build
Summary:        package kernel and initrd for OBS VM builds, dracut part
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
mkdir -p %{buildroot}/usr/lib/dracut/modules.d/80obs
cat > %{buildroot}/usr/lib/dracut/modules.d/80obs/module-setup.sh <<EOF
#!/bin/bash

# called by dracut
check() {
    return 0
}

# called by dracut
installkernel() {
    hostonly='' instmods obs
}

# called by dracut
install() {
    inst_hook pre-udev 10 "\$moddir"/setup_obs.sh
}
EOF
chmod a+rx %{buildroot}/usr/lib/dracut/modules.d/80obs/module-setup.sh
cat > %{buildroot}/usr/lib/dracut/modules.d/80obs/setup_obs.sh <<EOF
#!/bin/sh
info "Loading kernel modules for OBS"
info "  Loop..."
modprobe loop max_loop=64 lbs=0 || modprobe loop max_loop=64
info "  binfmt misc..."
modprobe binfmt_misc
EOF
chmod a+rx %{buildroot}/usr/lib/dracut/modules.d/80obs/setup_obs.sh

# a longer list to have them also available for qemu cross builds where x86_64 kernel runs in eg. arm env.
# this list of modules where available on build workers of build.opensuse.org, so we stay compatible.
export KERNEL_MODULES="loop dm-mod dm-snapshot binfmt-misc fuse kqemu squashfs ext2 ext3 ext4 reiserfs btrfs nf_conntrack_ipv6 binfmt_misc virtio_pci virtio_mmio virtio_blk virtio_rng fat vfat nls_cp437 nls_iso8859-1 ibmvscsi ibmvscsic"

# manually load all modules to make sure they're available
for i in $KERNEL_MODULES; do
(
  echo "info '  $i'"
  echo "modprobe $i"
) >> %{buildroot}/usr/lib/dracut/modules.d/80obs/setup_obs.sh
done

%files
%defattr(-,root,root)
%dir /usr/lib/dracut/modules.d
%dir /usr/lib/dracut/modules.d/80obs
/usr/lib/dracut/modules.d/80obs/*

%changelog
