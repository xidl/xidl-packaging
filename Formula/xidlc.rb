class Xidlc < Formula
  desc "XIDL compiler and multi-target code generator"
  homepage "https://github.com/xidl/xidl"
  url "https://github.com/xidl/xidl/archive/refs/tags/v0.107.0.tar.gz"
  sha256 "c7cfd5656ecf65625d6e0cf71ff3eddf719b76d569d6c6b5f2ce011e80b12037"
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
