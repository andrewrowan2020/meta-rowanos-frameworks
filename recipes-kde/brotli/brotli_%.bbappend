SRC_URI:remove = "git://github.com/google/brotli.git;branch=master;protocol=https"
SRC_URI:prepend = "https://codeload.github.com/google/brotli/tar.gz/${SRCREV};downloadfilename=brotli-${SRCREV}.tar.gz "

SRC_URI[sha256sum] = "aaa739962a45b508b2e783b915e6b2b57ed3b12bd4b0feac73acfb144dffa54f"

S = "${WORKDIR}/brotli-${SRCREV}"
