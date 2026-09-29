# RowanOS keeps the Qt XCB platform plugin for XWayland clients, while the MTK
# graphics stack supplies EGL/GLES2 and GBM instead of desktop libGL. Set these
# inputs directly so packageconfig dependency expansion sees them before the
# BSP's deferred DISTRO_FEATURES removals are filtered.
PACKAGECONFIG_GRAPHICS = "${@bb.utils.filter('DISTRO_FEATURES', 'vulkan wayland', d)} kms gbm gles2 eglfs linuxfb"
PACKAGECONFIG_X11 = "xcb"

# KActivities stores Plasma session state in SQLite. Without the Qt SQL SQLite
# driver, kactivitymanagerd aborts and plasmashell cannot load the desktop.
# XDG Desktop Portal KDE uses Qt PrintSupport private CUPS headers.
PACKAGECONFIG:append:class-target = " sql-sqlite cups"

QT_QPA_DEFAULT_PLATFORM = "wayland"
