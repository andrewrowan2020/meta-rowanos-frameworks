# Apply the same Steam-free launcher patch to the evaluation bundle.
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI:append = " file://0001-rowanos-standalone-launch.patch"
