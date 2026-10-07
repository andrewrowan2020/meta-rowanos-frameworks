# The D16 image uses the pinned ARM64 FEX runtime with machine-scoped packages.
COMPATIBLE_MACHINE = "^genio-1200-radxa-nio-12l-d16$"
PACKAGE_ARCH = "${MACHINE_ARCH}"

# On the Panfrost/Mesa D16 image, FEX GL thunks link against Mesa GL.
DEPENDS:remove = "libmali gl4es"
DEPENDS:append = " mesa "
RDEPENDS:${PN}:remove = "gl4es"
EXTRA_OECMAKE:remove = "-DOPENGL_gl_LIBRARY=${RECIPE_SYSROOT}${libdir}/gl4es/libGL.so.1"
EXTRA_OECMAKE:append = " -DOPENGL_gl_LIBRARY=${RECIPE_SYSROOT}${libdir}/libGL.so.1 "
