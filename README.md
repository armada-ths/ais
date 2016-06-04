[AIS](http://ais.armada.nu/) — Armada Internal System
==================================================

Contribution Guides
--------------------------------------

In the spirit of open source software development, AIS always encourages community code contribution. To help you get started and before you jump into writing code, be sure to read these important contribution guidelines thoroughly:

1. Nothing to see here, continue to next section.
2. Actually yes there is, work on branches and send a PR for anything non-trivial. No long-running branches.

Also, check out the [CONTRIBUTING.md](CONTRIBUTING.md).

Development setup
-------------
1. Download [VirtualBox](https://www.virtualbox.org) and [Vagrant](https://www.vagrantup.com/downloads.html)
3. Clone the repo and run `vagrant up` from the repo's root
4. ☕️
5. Browse to [localhost:8080/admin](http://localhost:8080/admin) and log in with username "admin" and password "admin"
6. Browse to [localhost:8080/](http://localhost:8080/). Bam! That's your local AIS environment.

If you don't want to use Vagrant, instructions for getting started with [OSX](docs/getting_started_mac.md), [Ubuntu](docs/getting_started_linux.md), and [Windows](docs/getting_started_windows.md) are available. See [docs/producton_setup.md](docs/production_setup.md) for details on how to get a production server up and running.
