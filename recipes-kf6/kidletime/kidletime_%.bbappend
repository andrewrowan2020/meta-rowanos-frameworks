# KIdleTime enables both Wayland and X11 pollers by default. Keep both so
# Plasma can serve Wayland sessions and XWayland clients.
DEPENDS:append = " libx11 libxext libxcb"
