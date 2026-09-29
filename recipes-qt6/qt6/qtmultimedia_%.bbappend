# Build the official immutable Qt release archive instead of cloning the module
# repository. Keep the desktop multimedia backends, but omit the optional Quick
# 3D spatial-audio bridge from the first Plasma validation image.
SRC_URI = "https://download.qt.io/official_releases/qt/6.8/6.8.3/submodules/qtmultimedia-everywhere-src-${PV}.tar.xz"
SRC_URI[sha256sum] = "32e82307d783172a3b984cc3c47c5e4e8b819cee3cbfc702c7012c47f15f6b01"
S = "${WORKDIR}/qtmultimedia-everywhere-src-${PV}"

PACKAGECONFIG:remove = "spatialaudio_quick3d"
