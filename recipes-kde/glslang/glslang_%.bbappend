# Use the immutable Khronos commit archive instead of cloning the complete Git
# mirror. This is equivalent to SRCREV and is reliable on the build network.
SRC_URI:remove = "git://github.com/KhronosGroup/glslang.git;protocol=https;branch=main"
SRC_URI:prepend = "https://codeload.github.com/KhronosGroup/glslang/tar.gz/${SRCREV};downloadfilename=glslang-${SRCREV}.tar.gz "

SRC_URI[sha256sum] = "8bba14a39f7a666587b15e66098e816e900974d9450b401db3d25d5a4ce5c145"
S = "${WORKDIR}/glslang-${SRCREV}"
