# Build both backends: Plasma uses Wayland, while XWayland clients and KF6
# compatibility APIs require KX11Extras.
DEPENDS:append = " libx11 libxfixes libxcb xcb-util-keysyms xcb-util-wm"
EXTRA_OECMAKE:append:class-target = " -DKWINDOWSYSTEM_X11=ON -DKWINDOWSYSTEM_WAYLAND=ON"
