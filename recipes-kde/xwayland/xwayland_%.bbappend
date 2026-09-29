# The MTK Mali userspace exposes EGL/GLES and GBM, but no desktop libGL.
# Keep XWayland and its EGL glamor path while omitting GLX for this validation
# image. Plain X11 clients continue to work under KWin Wayland.
PACKAGECONFIG:remove = "glx"
