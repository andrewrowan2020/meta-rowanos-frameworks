# SPDX-FileCopyrightText: 2026 RowanOS contributors
# SPDX-License-Identifier: MIT

# The MediaTek Mali DDK has no X11 display backend, so the BSP removes x11.
# Plasma runs on Wayland, but the upstream Plasma and SDDM recipes still need
# XCB and XWayland userspace packages. Remove only x11 from BitBake's deferred
# feature-removal operations; EGL/GBM remains provided by libmali.
python () {
    remove_ops = d.getVarFlag("DISTRO_FEATURES", ":remove", False) or []
    filtered_ops = []
    for value, override in remove_ops:
        kept_features = [feature for feature in value.split() if feature != "x11"]
        if kept_features:
            filtered_ops.append([" ".join(kept_features), override])
    d.setVarFlag("DISTRO_FEATURES", ":remove", filtered_ops)
}