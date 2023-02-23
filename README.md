[AIS](http://ais.armada.nu/) — Armada Internal System [![Build Status](https://travis-ci.org/armada-ths/ais.svg?branch=master)](https://travis-ci.org/armada-ths/ais)
==================================================

hejsan

Contribution Guides
--------------------------------------
- Please try to write clean, readable code
- Please try to write tests for your code
- Please try to write meaningful commit messages, PR descriptions etc.
- Please try to help resolve any open PRs / issues 

Above all, be respectful towards others :)

Branching strategy
--------------------------------------
We have one long-running branch, `master`, that is more or less continuously deployed. In order to be merged into `master` your code **must** be peer reviewed by someone else on the team in a PR (this is enforced on GitHub).

Development setup
-------------
1. Download [VirtualBox](https://www.virtualbox.org) and [Vagrant](https://www.vagrantup.com/downloads.html)
2. Clone the repo and run `vagrant up` from the repo's root
3. ☕️
4. type in terminal: vagrant ssh
5. type in terminal: ./dev-runserver.sh 
6. Browse to [localhost:8080](http://localhost:8080) and log in with username "admin" and password "admin"
7. Bam! That's your local AIS environment.

If you don't want to use Vagrant, instructions for getting started with [OSX](docs/getting_started_mac.md), [Ubuntu](docs/getting_started_linux.md), and [Windows](docs/getting_started_windows.md) are available. See [docs/producton_setup.md](docs/production_setup.md) for details on how to get a production server up and running.

Scripts
----------------------------
A number of scripts are available in the scripts folder. Others can be run with ```manage.py [scriptname]```. Run ```manage.py help``` to list what scripts are available through manage.py 

License Information
-------------------
Please check out [LICENSE.txt](LICENSE.txt) for information.
