DEPENDS:append = " bubblewrap bubblewrap-native"

RDEPENDS:${PN}:append = " bubblewrap xauth"

PACKAGECONFIG:append = " xauth"

# Flatpak 1.15.8 uses --bind-fd to close CVE-2024-42472 races. Its bundled
# Bubblewrap 0.9.0 predates that option, so use the system 0.10.0 build.
EXTRA_OEMESON:append = " -Dsystem_bubblewrap=bwrap"
