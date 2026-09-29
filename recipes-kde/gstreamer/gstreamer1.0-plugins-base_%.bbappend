# MTK's binary Mali stack exposes EGL/GLES2, but not desktop libGL/GLX.
# Keep X11/XWayland enabled for Plasma while selecting the supported GStreamer GL path.
PACKAGECONFIG:remove = "opengl glx x11"
