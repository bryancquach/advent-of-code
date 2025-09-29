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
  config.vm.synced_folder ".", "/vagrant",
    owner: "vagrant", group: "vagrant",
    mount_options: ["dmode=775", "fmode=664"]

  config.vm.define "dev" do |dev|

    dev.vm.provider "docker" do |d|
      image_name = "bryancquach/advent_of_code_2024:latest"
      
      # Check if the image exists locally or can be pulled
      image_exists = system("docker image inspect #{image_name} > /dev/null 2>&1") || 
                     system("docker pull #{image_name} > /dev/null 2>&1")
      
      if image_exists
        puts "Using existing image: #{image_name}"
        d.image = image_name
      else
        puts "Image #{image_name} not found, building from Dockerfile..."
        d.dockerfile = "docker/Dockerfile"
        d.build_dir = "."
        d.build_args = [
          "--no-cache",
          "--tag",
          "#{image_name}"
        ]
      end
      d.cmd = ["/usr/sbin/sshd", "-D", "-o", "ListenAddress=0.0.0.0"] # spin up SSH server
      d.has_ssh = true
      d.create_args = [
        "--rm", # ensure container is deleted when shutting down
      ]
    end
  end
end
