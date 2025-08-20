class Iamx < Formula
  desc "IAM Policy Explainer - Local-first IAM policy analyzer"
  homepage "https://github.com/iamsteve0/iamx"
  url "https://files.pythonhosted.org/packages/a4/fd/7ba670bbdfde42caf8ea443da941d085239848ebb2a6b7433baa388e06de/iamx-0.1.0-py3-none-any.whl"
  sha256 "your_sha256_here"
  license "MIT"

  depends_on "python@3.8"

  def install
    system "python3", "-m", "pip", "install", "--prefix=#{libexec}", "iamx"
    bin.install Dir["#{libexec}/bin/*"]
    bin.env_script_all_files(libexec/"bin", PYTHONPATH: ENV["PYTHONPATH"])
  end

  test do
    system "#{bin}/iamx", "--version"
  end
end
