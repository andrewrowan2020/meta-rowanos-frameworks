# Fetch the exact upstream commit as an immutable archive. This avoids relying
# on GitHub's Git smart protocol on restricted build networks.
SRC_URI = "https://codeload.github.com/zxing-cpp/zxing-cpp/tar.gz/d6068bcebeb8fd9f0d35a99b00d202be86a14dbe;downloadfilename=zxing-cpp-d6068bcebeb8fd9f0d35a99b00d202be86a14dbe.tar.gz"
SRC_URI[sha256sum] = "67a58db28ba01234f9692d89f1c7c67cf4cb1cbc6d3c3784352951cdabee5847"

S = "${WORKDIR}/zxing-cpp-d6068bcebeb8fd9f0d35a99b00d202be86a14dbe"
