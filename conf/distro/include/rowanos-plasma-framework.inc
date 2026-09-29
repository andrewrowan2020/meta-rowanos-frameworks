# SPDX-License-Identifier: MIT
# meta-kde uses UNPACKDIR on newer Yocto releases; Scarthgap unpacks into WORKDIR.
UNPACKDIR ?= "${WORKDIR}"
INHERIT += "rowanos-kf6-host-compat rowanos-x11-compat"
QT_GIT_PROTOCOL = "https"
