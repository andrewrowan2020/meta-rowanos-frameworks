SRC_URI:remove = "git://github.com/Exiv2/exiv2.git;protocol=https;branch=0.28.x"
SRC_URI:prepend = "https://codeload.github.com/Exiv2/exiv2/tar.gz/${SRCREV};downloadfilename=exiv2-${SRCREV}.tar.gz "

SRC_URI[sha256sum] = "99bca584ba698cc3390ec92977f3e80ddf490f360b7f3bbaf81868d9a11d9e81"

S = "${WORKDIR}/exiv2-${SRCREV}"
