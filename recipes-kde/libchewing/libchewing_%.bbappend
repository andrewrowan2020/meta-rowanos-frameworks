SRC_URI = " \
    https://codeload.github.com/chewing/libchewing/tar.gz/${SRCREV};downloadfilename=libchewing-${SRCREV}.tar.gz \
    file://0001-Cross-compilation-options.patch \
    file://0002-Disable-genkeystroke-testapp.patch \
"
SRC_URI[sha256sum] = "c55a4d0c64995725e9d78c3753f0b67f7a71fac5541678fab9859513c75ba2d1"

S = "${WORKDIR}/libchewing-${SRCREV}"
