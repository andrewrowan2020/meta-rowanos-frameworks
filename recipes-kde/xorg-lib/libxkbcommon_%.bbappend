# RowanOS needs xkbcommon-x11 for the Qt XCB platform plugin used by XWayland.
# Set the complete feature set explicitly so packageconfig dependency expansion
# and Meson arguments agree despite the BSP's deferred x11 feature removal.
PACKAGECONFIG = "wayland x11 xkbregistry"
