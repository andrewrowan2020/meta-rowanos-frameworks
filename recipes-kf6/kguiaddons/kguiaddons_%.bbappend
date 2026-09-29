# The RowanOS validation image is Wayland-only and Qt is built without xcb.
EXTRA_OECMAKE:append:class-target = " -DWITH_X11=OFF -DWITH_WAYLAND=ON"
