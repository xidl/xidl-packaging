class Xidlc < Formula
  desc "XIDL compiler and multi-target code generator"
  homepage "https://github.com/xidl/xidl"
  url "https://github.com/xidl/xidl/archive/refs/tags/v0.79.1.tar.gz"
  sha256 "49758e44198a46c0569d88de0dde52f4b1205315c3033ac4ad615c30dde093ba"
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
