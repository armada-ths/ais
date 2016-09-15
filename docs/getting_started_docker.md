## Introduction
Thanks to our good friend @macaullyjames you can have a perfectly working Vagrant environment up and running within a minute on your local computer. This is truly awesome. 

Just as virtual machines has it's strengths, it also has it's drawbacks. Slow boot times and heavy disk usage is some of these drawbacks. As an alternative for those who don't want to run AIS in a virtual machine, there is Docker. Docker uses Linux cgroups and kernel namespaces to create a separate container for running applications on your OS.

## Installation
Go to [Docker](https://docs.docker.com/engine/installation/) and read the installation instructions for installing the Docker engine on your OS. Docker is only provided natively on Linux operating systems, but installers for [Windows](https://docs.docker.com/engine/installation/windows/) and [OSX](https://docs.docker.com/engine/installation/windows/) exist. Follow the installations instructions and check that it's working correctly with:
```
$ docker -v
Docker version 1.12.1
```

## Running AIS in Docker
Now that we have Docker installed, it's time to spread your wings and kick up AIS in a brand new Docker container. Clone the repo and `cd` into the `ais` folder. When you are inside the repositories root folder you can start the container by issuing the following command:
```
$ docker run --name ais --volume "$PWD":/usr/src/app --workdir /usr/src/app --publish 8080:8080 --env DJANGO_SETTINGS_MODULE=local_settings --detach django bash -c "pip install -r requirements.txt && python manage.py runserver 0.0.0.0:8080"
```
If this is the first time you're running the command, you'll have to wait a couple of minutes while the Django image gets pulled from Docker Hub and the container gets set up.   

## What's happening
This will start a container named `ais` and mount the current working directory as a volume inside the container. We're publishing port 8080 to the host and setting `DJANGO_SETTINGS_MODULE` to `local_settings` so that we don't have to provide `--settings=local_settings` for each command we run on the container. We'll also install the python packages from the `requirements.txt` file and start a local Django server.

## What's next
To issue commands against the container we use `docker exec`. The first time we start a AIS we'll be prompted to log in with our KTH id. Since we are developing locally the CAS login won't work correctly. So to create a new Django user we can use the following command:
```
$ docker exec -it ais ./manage.py createsuperuser
```

To see the container logs we can use the following command
```
$ docker logs ais 
```

To see the running containers on the host we use
```
$ docker ps
```
If the container doesn't show up, it has probably been suspended. Attach the `-a` flag and you will see suspended containers as well. 

Say you want to stop the running container
```
$ docker stop ais
```

And if you want to start the container again
```
$ docker start ais
```

If you have any questions just drop a line in the Slack channel. And feel free to improve this document with more Docker stuff!
