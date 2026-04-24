class Xidlc < Formula
  desc "XIDL compiler and multi-target code generator"
  homepage "https://github.com/xidl/xidl"
  url "https://github.com/xidl/xidl/archive/refs/tags/v0.48.0.tar.gz"
  sha256 "d6aa5724d0969ab69cb10b56666c0c0e7093139f0525801140a3075fdc200c00"
  license "Apache-2.0"
  head "https://github.com/xidl/xidl.git", branch: "master"

  depends_on "rust" => :build

  def install
    system "cargo", "install", *std_cargo_args(path: "xidlc")
  end

  test do
    assert_match version.to_s, shell_output("#{bin}/xidlc --version")
  end
end
