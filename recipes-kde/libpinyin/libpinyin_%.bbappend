SRC_URI = " \
    https://codeload.github.com/libpinyin/libpinyin/tar.gz/${SRCREV};downloadfilename=libpinyin-${SRCREV}.tar.gz;name=source \
    https://downloads.sourceforge.net/project/libpinyin/models/model19.text.tar.gz;downloadfilename=model19.text.tar.gz;subdir=libpinyin-${SRCREV};unpack=0;name=model \
    file://0000-Utilize-bitbake-download-and-use-tools-from-PATH.patch \
    file://0001-Optionally-install-utilities.patch \
    file://0002-Provide-option-to-use-pre-downloaded-archive.patch \
    file://0003-Add-option-to-disable-data-generation.patch \
"
SRC_URI:class-native = " \
    https://codeload.github.com/libpinyin/libpinyin/tar.gz/${SRCREV};downloadfilename=libpinyin-${SRCREV}.tar.gz;name=source \
    file://0001-Optionally-install-utilities.patch \
    file://0002-Provide-option-to-use-pre-downloaded-archive.patch \
    file://0003-Add-option-to-disable-data-generation.patch \
"
SRC_URI[source.sha256sum] = "a428f47fa67aa0b421ce1d4c686f66662ff8aaa056839612081411f0d5bcaa9f"
SRC_URI[model.sha256sum] = "56422a4ee5966c2c809dd065692590ee8def934e52edbbe249b8488daaa1f50b"

S = "${WORKDIR}/libpinyin-${SRCREV}"
