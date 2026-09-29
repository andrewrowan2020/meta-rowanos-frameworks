# Plasma Workspace builds X11 compatibility helpers even for a Wayland session.
# Declare every X11 component that its top-level CMake checks as mandatory.
DEPENDS:append = " libice libsm libxcursor libxtst"
