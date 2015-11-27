# kernel-obs-build
OBS build kernels for non-SUSE distributions

The OBS can use the distribution's kenrel for build VMs, however it needs to be prepared for this task.
So for newer SUSE distributions, there is a package ``kernel-obs-build``, which does exactly that.

Basically the original kernel is copied to

    /.build.kernel.kvm  # KVM worker version, usually kernel-default
    /.build.kernel.xen  # Xen worker version, usually kernel-xen

and two initrds are generated, namely ``.build.initrd.xen`` and ``.build.initrd.kvm``

These spec files here try to do the same for non-SUSE distributions.

Note that I have split kernel-obs-build into two packages: ``kernel-obs-build`` and
``dracut-obs-build``, with the former BuildRequiring the latter. This is to avoid
the need of root rights for rpm building, which needs admin access to your build
service installation.

So how to use this? Create a package ``kernel-obs-build`` in your project, add the .spec and .changes files and commit. Then ``osc linkpac yourproject kernel-obs-build yourproject dracut-obs-build``. The two packages should now build one after another. Then edit your project config with ``osc meta prjconf -e yourproject`` and add the line ``VMInstall: obs-kernel-build``. From now on, the distro kernel is used for building.

Good Luck :-)
