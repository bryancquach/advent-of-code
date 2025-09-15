ARG base_image=public.ecr.aws/docker/library/python:3.13.0a1-slim
FROM ${base_image}

# Debian packages and tools
RUN  DEBIAN_FRONTEND=noninteractive apt-get -qq update \
	&& DEBIAN_FRONTEND=noninteractive apt-get -qq install openssh-server sudo \
	&& DEBIAN_FRONTEND=noninteractive apt-get -qq autoremove \
	&& rm -rf /var/lib/apt/lists/*

# Add create vagrant group and user with sudo privileges
RUN mkdir -p /run/sshd \
    && useradd --user-group --create-home --shell /bin/bash --groups sudo vagrant \
    && echo "vagrant ALL=(ALL) NOPASSWD:ALL" >/etc/sudoers.d/vagrant-user \
    && echo 'vagrant:vagrant' | chpasswd \
    && echo "AcceptEnv LANG LC_* POETRY_*" >>/etc/ssh/sshd_config

# Python3 environment packages and tools
RUN DEBIAN_FRONTEND=noninteractive apt-get -qq update \
    && DEBIAN_FRONTEND=noninteractive apt-get -qq install \
        git \
        vim \
    && pip3 install -v poetry debugpy autoflake black \
    && DEBIAN_FRONTEND=noninteractive apt-get -qq autoremove \
    && rm -rf /var/lib/apt/lists/*

# For Vagrant
EXPOSE 22