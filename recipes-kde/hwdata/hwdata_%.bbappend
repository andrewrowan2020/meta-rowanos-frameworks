# Fetch the exact upstream commit as a bounded archive. A full mirrored clone
# of the hwdata repository is unreliable on the current build network.
SRC_URI = "https://codeload.github.com/vcrhonek/hwdata/tar.gz/${SRCREV};downloadfilename=hwdata-${SRCREV}.tar.gz"
SRC_URI[sha256sum] = "b58c6bc1282d7410b24c62e9b31959c923ce362d73c8858bb736d0baaebe6b2d"

S = "${WORKDIR}/hwdata-${SRCREV}"
