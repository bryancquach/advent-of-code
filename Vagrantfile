# Environment setup for dev work

ENV["POETRY_CACHE_DIR"] = "/vagrant/build/cache"

Vagrant.configure("2") do |config|
  config.ssh.forward_agent = true
  config.ssh.username = "vagrant"
  config.ssh.password = "vagrant"
  config.ssh.insert_key = true
  config.ssh.extra_args = ["-t", "cd /vagrant; bash"]
  config.ssh.forward_env = [
    "POETRY_CACHE_DIR"
  ]

  config.vm.define "dev" do |dev|

    dev.vm.provider "docker" do |d|
      d.dockerfile = "docker/Dockerfile"
      d.build_dir = "."
      d.cmd = ["/usr/sbin/sshd", "-D", "-o", "ListenAddress=0.0.0.0"] # spin up SSH server
      d.has_ssh = true
      d.create_args = [
        "--rm", # ensure container is deleted when shutting down
      ]
      d.build_args = [
        "--platform",
        "linux/amd64,linux/arm64",
        "--cache-from",
        "type=registry,ref=bryancquach/advent_of_code_2024:latest",
        "--tag",
        "bryancquach/advent_of_code_2024:latest"
      ]
    end
  end
end
