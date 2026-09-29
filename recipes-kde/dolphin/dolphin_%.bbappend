# Dolphin 25.08 treats KF6FileMetaData as a required component, but the
# upstream Yocto recipe does not declare it in DEPENDS.
DEPENDS:append = " kfilemetadata"
