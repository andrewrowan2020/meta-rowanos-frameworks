SRC_URI:remove = "git://github.com/uclouvain/openjpeg.git;branch=master;protocol=https"
SRC_URI:prepend = "https://codeload.github.com/uclouvain/openjpeg/tar.gz/${SRCREV};downloadfilename=openjpeg-${SRCREV}.tar.gz "

SRC_URI[sha256sum] = "c2bb373d68286ef475713f251504f59be6e44980dc5c56314bd4a7681fc69fce"

S = "${WORKDIR}/openjpeg-${SRCREV}"
