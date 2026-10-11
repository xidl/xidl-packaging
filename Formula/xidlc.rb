class Xidlc < Formula
  desc "XIDL compiler and multi-target code generator"
  homepage "https://github.com/xidl/xidl"
  url "https://github.com/xidl/xidl/archive/refs/tags/v0.99.1.tar.gz"
  sha256 "8311c1985133808bdd30f65be261462493b1170fc05e4f63ff263dde034df877"
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
