# meta-rowanos-common

Common RowanOS integration layer for Qt 6, KDE Frameworks 6/Kirigami and KDE/Plasma.

## Current layout

- conf/layer.conf: BitBake layer configuration.
- recipes-qt6/: common Qt 6 options and compatibility patches.
- recipes-kf6/: common KF6/Kirigami options and compatibility patches.
- recipes-kde/: common KDE/Plasma options and compatibility patches.
- COPYING.MIT: layer license.

The recipe subdirectories currently contain placeholders, with no actual .bb
or .bbappend recipes. Unrelated recipe categories and unused metadata placeholders
have been removed. Upstream recipe layers remain in the sibling directories
meta-qt6, meta-kf6 and meta-kde.

Board-specific options and product configuration belong in rowanos-device.
This common layer must not depend on rowanos-device.

BitBake collection identifier remains rowanos_frameworks. The upstream repository
identity remains meta-rowanos-frameworks. The workspace manifest pins this
repository at rowanos-frameworks/meta-rowanos-common.

Add the four actual framework layer directories to BBLAYERS; the parent
rowanos-frameworks collection directory is not a Yocto layer.
