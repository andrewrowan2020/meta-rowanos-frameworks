# meta-rowanos-common

Universal RowanOS Qt 6 / KF6 / Kirigami / KDE Plasma compatibility for the
pinned Scarthgap layers, referenced from rowanos001.

* `recipes-qt6`: Qt EGL/GLES, XCB and multimedia integration.
* `recipes-kf6`: missing X11 build dependencies and Wayland configuration.
* `recipes-kde`: Plasma/Dolphin fixes and their required graphics, audio,
  Wayland and support dependencies. These are KDE dependency fixes, not
  additional product features.
* `classes`: KF6 class-name aliases and host-tool/X11 compatibility.
* `conf/distro/include/rowanos-plasma-framework.inc`: common compatibility
  settings, selected by the device's RowanOS distro.

No device/image/session policy or game runtime belongs here. Upstream meta-qt6,
meta-kf6, meta-kde and mtk-yocto-bsp remain separate, unmodified repositories.
