# RowanOS launches registered games without Steam or Steam Linux Runtime.
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI:append = " file://0001-rowanos-standalone-launch.patch file://0002-piper-local-deps.patch file://0003-sshfs-dist-symlink-ownership.patch file://0004-gst-rs-dav1d-only-workspace.patch"
