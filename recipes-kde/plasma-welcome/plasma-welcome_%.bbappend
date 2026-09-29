# SPDX-License-Identifier: MIT

# Plasma 6.4 installs its public welcome QML module under the Qt QML
# directory, but the upstream meta-kde recipe does not package it.
FILES:${PN}:append = " ${libdir}/qml/org/kde/plasma/welcome/*"
