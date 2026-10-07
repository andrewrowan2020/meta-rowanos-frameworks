# RowanOS launches a registered game directly without a Steam client.
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI:append = " file://0001-rowanos-standalone-launch.patch"
