FILESEXTRAPATHS:prepend := "${THISDIR}/files:"

# Backport upstream PipeWire fix for mixed designated initializers. KWin 6.4
# builds as C++23 and GCC rejects the old SPA header syntax.
SRC_URI += "file://0001-treewide-fix-CXX20-designated-initializers.patch"
