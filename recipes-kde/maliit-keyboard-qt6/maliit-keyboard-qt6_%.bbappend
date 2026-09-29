SRC_URI = " \
    https://codeload.github.com/maliit/keyboard/tar.gz/${SRCREV};downloadfilename=maliit-keyboard-${SRCREV}.tar.gz \
    file://0001-qml-Fix-for-qt6.patch \
    file://0001-cmake-add-Qt6-support.patch \
"
SRC_URI[sha256sum] = "6513fb62c9234e2c0ab363c6753168cfdb62b0fca9f8808b8b3f32e529829d32"

S = "${WORKDIR}/keyboard-${SRCREV}"
