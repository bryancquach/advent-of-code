# Overview

This repository contains solutions to [Advent of Code 2024](https://adventofcode.com/2024) challenges written in Python 3. Key points about the infrastructure and codebase:
* Developed within a Docker-backed [Vagrant](https://developer.hashicorp.com/vagrant) virtual machine (VM) for portability
* Employs [Poetry](https://python-poetry.org/) within the VM for dependency management and packaging
* Uses [Typer](https://typer.tiangolo.com/) as the command-line interface (CLI) framework. Each daily challenge is developed as its own CLI micro-application that is integrated into a main CLI app
* Core functionality of each daily challenge tested using a [pytest](https://docs.pytest.org/en/stable/) unit-testing framework
* Python code formatted using [Black](https://github.com/psf/black) for [PEP 8](https://peps.python.org/pep-0008/) compliant style consistency
* GitHub Copilot is used as a reviewer for merge requests into the main branch

# Repository structure

The codebase uses the following general structure:

* Infrastructure as Code (IaC) for setting up the dev environment is primarily located in the repo base directory as Vagrant and Docker-related files and directories
* The core functionality for challenge solving, the CLI, input data files, and unit tests are contained within an `advent-of-code` package within the repo. The CLI provides a user interface to run solutions for all the daily challenges. Since packaging and dependency management are done using Poetry, the Poetry configuration (`pyproject.toml`) is located within the package directory
* Each daily challenge is considered a subpackage of the `advent-of-code` package with each subpackage given its own package subdirectory. Each subpackage functions as a CLI micro-application that can be called as a subcommand from the main CLI application. 

The tree below visualizes the general structure:
```
advent-of-code
├── LICENSE
├── README.md
├── Vagrantfile                        <--- IaC for dev environment
├── advent_of_code
│   ├── poetry.lock
│   ├── pyproject.toml                 <--- Poetry package config
│   ├── README.md
│   ├── src
│   │   └── advent_of_code
│   │       ├── __init__.py
│   │       ├── main.py                <--- Main CLI app
│   │       ├── data                   <--- Daily challenge input data
│   │       │   ├── __init__.py
│   │       │   └── day_01
│   │       │       ├── __init__.py
│   │       │       └── input.tsv
│   │       └── day_01                 <--- Each daily challenge gets its own subpackage dir
│   │           ├── __init__.py
│   │           ├── cli.py             <--- Daily challenge specific CLI micro-app
│   │           └── metrics.py
│   └── tests                          <--- Tests for package code
│       ├── __init__.py
│       └── unit
│           ├── __init__.py
│           └── day_01                 <--- Each daily challenge gets its own test dir
│               ├── __init__.py
│               └── test_metrics.py
└── docker                             <--- IaC for dev environment
    └── Dockerfile
```

# User guide

## Environment setup

Creating a Vagrant VM to use the CLI requires having [Vagrant](https://developer.hashicorp.com/vagrant/install), [Docker Engine](https://docs.docker.com/engine/install/), and [Git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (with SSH-based cloning from GitHub configured) installed. Once those are installed, run the following command-line commands:

```bash
# Set up Vagrant VM called 'dev'
git clone git@github.com:bryancquach/advent-of-code.git
cd advent-of-code
vagrant up

# Check VM status
vagrant status

# Start shell session in VM
vagrant ssh dev
```

The above code snippet should install and spin up a Vagrant VM called `dev` that you can communicate with via SSH. This can be verified by checking that the command `vagrant status` outputs `dev` as a running VM. If setup is successful, you can start a shell session within the VM using `vagrant ssh dev`.

Within the VM, dependencies for the `advent-of-code` package need to installed:

```bash
cd /vagrant/advent_of_code/
poetry install
```

Once this completes, your environment setup is complete!

## Running a daily challenge solution

Daily challenge solutions can be run with the main CLI from within the Vagrant VM through a Poetry-managed virtual environment:

```
cd /vagrant/advent_of_code/

# Main CLI usage doc
poetry run advent-of-code --help

# Day 1 CLI usage doc
poetry run advent-of-code day-1 --help

# Usage docs for Day 1 CLI commands
poetry run advent-of-code day-1 run-part1 --help
poetry run advent-of-code day-1 run-part2 --help

# Example runs
poetry run advent-of-code day-1 run-part1 \
  src/advent_of_code/data/day_01/input.tsv

poetry run advent-of-code day-1 run-part2 \
  src/advent_of_code/data/day_01/input.tsv 
```
