SRC_URI = " \
    https://codeload.github.com/maliit/framework/tar.gz/${SRCREV};downloadfilename=maliit-framework-${SRCREV}.tar.gz \
    file://0001-common-namespace-add-missing-include-QList.patch \
    file://0002-maliitpluginsconfig-fix-for-qt6.patch \
    file://0003-shellintegration-qwaylandinputpanelshellintegration-.patch \
"
SRC_URI[sha256sum] = "2ba375c59b5d05618dca061926e4e6c1cd66cf5a716444d98eb652f76084f487"

S = "${WORKDIR}/framework-${SRCREV}"
