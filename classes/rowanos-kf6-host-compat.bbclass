# The Ubuntu 18.04 build host cannot load newer uninative libraries into its
# /bin/bash. KF6 exports STAGING_LIBDIR_NATIVE while building and some native
# tools and Ninja commands invoke the host Bash, so isolate the host process
# environment from that library path.

rowanos_kf6_native_compile_env() {
    unset LD_LIBRARY_PATH
}

rowanos_prepare_kf6_msgfmt() {
    install -d ${B}
    cat > ${B}/rowanos-msgfmt <<EOF
#!/bin/sh
unset LD_LIBRARY_PATH
exec "${STAGING_BINDIR_NATIVE}/msgfmt" "\$@"
EOF
    chmod 0755 ${B}/rowanos-msgfmt
}

rowanos_prepare_kf6_xmllint() {
    install -d ${B}/rowanos-host-tools
    cat > ${B}/rowanos-host-tools/rowanos-xmllint <<EOF
#!/bin/sh
unset LD_LIBRARY_PATH
exec "${STAGING_BINDIR_NATIVE}/xmllint" "\$@"
EOF
    chmod 0755 ${B}/rowanos-host-tools/rowanos-xmllint
    ln -sf rowanos-xmllint ${B}/rowanos-host-tools/xmllint
    export PATH="${B}/rowanos-host-tools:$PATH"
}

python __anonymous() {
    if bb.data.inherits_class("kf6_cmake_framework", d):
        # kf6_cmake_framework exports STAGING_LIBDIR_NATIVE in do_compile for
        # native and target recipes. Run this after that export and before
        # Ninja launches the Ubuntu 18.04 /bin/bash.
        d.prependVar("cmake_do_compile", "    rowanos_kf6_native_compile_env\n")
    if (bb.data.inherits_class("kf6_cmake_framework", d)
            and not bb.data.inherits_class("native", d)
            and not bb.data.inherits_class("nativesdk", d)):
        d.appendVar("EXTRA_OECMAKE", " -DGETTEXT_MSGFMT_EXECUTABLE=${B}/rowanos-msgfmt")
        d.prependVar("cmake_do_configure", "    rowanos_prepare_kf6_msgfmt\n")
    if (bb.data.inherits_class("kf6_cmake_framework", d)
            and bb.data.inherits_class("native", d)
            and d.getVar("BPN") == "kdoctools"):
        d.appendVar("EXTRA_OECMAKE", " -DLIBXML2_XMLLINT_EXECUTABLE=${B}/rowanos-host-tools/rowanos-xmllint")
        d.prependVar("cmake_do_configure", "    rowanos_prepare_kf6_xmllint\n")
        d.prependVar("do_compile", "    rowanos_prepare_kf6_xmllint\n")
}
