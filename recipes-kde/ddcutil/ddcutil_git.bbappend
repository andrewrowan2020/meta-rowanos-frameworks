# GitHub mirror cloning is unreliable on the BSP host. Fetch the exact SRCREV
# as an immutable archive while retaining the upstream Yocto patch.
SRC_URI = "https://codeload.github.com/rockowitz/ddcutil/tar.gz/${SRCREV};downloadfilename=ddcutil-${SRCREV}.tar.gz \
           file://0001-Fix-out-of-tree-build.patch \
"
SRC_URI[sha256sum] = "ee42543663c38a5edf86cce842d60db647ea5df163edd79ec679dee17dbad423"
S = "${WORKDIR}/ddcutil-${SRCREV}"
