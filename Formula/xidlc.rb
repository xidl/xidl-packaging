class Xidlc < Formula
  desc "XIDL compiler and multi-target code generator"
  homepage "https://github.com/xidl/xidl"
  url "https://github.com/xidl/xidl/archive/refs/tags/v0.92.0.tar.gz"
  sha256 "31e4527e4d8ae1a9b3daca22a1be3c8ea2567bea6c7d55c99e8717013ba6cd64"
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
