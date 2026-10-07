# D16 scanout and Vulkan capability adaptation for the standalone compositor.
FILESEXTRAPATHS:prepend := "${THISDIR}/files:"
SRC_URI:append:genio-1200-radxa-nio-12l-d16 = " \
    file://0003-vulkan-d16-capability-adaptation.patch \
    file://0004-vulkan-check-scanout-capabilities.patch \
    file://0008-drm-basic-guard-optional-rotation.patch \
"

# The pinned upstream emits an x86_64-named WSI layer on AArch64.
do_install:append:genio-1200-radxa-nio-12l-d16() {
    rm -f ${D}${libdir}/libVkLayer_FROG_gamescope_wsi_x86_64.so
    rm -f ${D}${datadir}/vulkan/implicit_layer.d/VkLayer_FROG_gamescope_wsi.x86_64.json
}
