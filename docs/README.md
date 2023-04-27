# [AIS](http://ais.armada.nu/) — Armada Internal System

## Contribution Guides

See [CONTRIBUTING.md](CONTRIBUTING.md)

## Development setup

### Section 1: Installation of Dependencies

In order to run the project locally, you need the following tools:

- [Docker](https://docs.docker.com/get-docker/) (used to run the server and database)
- [Pip](https://pip.pypa.io/en/stable/installation/) (used to install `black`)
- [Black](https://pypi.org/project/black/) (used to format code)

### Section 2: Setup of Tools

If you are using Visual Studio Code, python code will automatically format upon saving the file. If you are using another editor, you need to either setup automatic formatting upon saving, or run `black .` before every commit (we recommend putting this command in a pre-commit hook).

### Section 3: Creation of Initial Files

Create a `.env` file in the root directory of the project, and insert the following values:

```env
SECRET_KEY=123
DJANGO_SETTINGS_MODULE=ais.local.settings
DB_HOST=db
```

### Section 4: Execution of the Server

The server will run in a `docker compose` instance. Before starting the server, go to the `entrypoint.sh` file and uncomment the following line:

```sh
python manage.py migrate --settings=local_settings
```

To start the server, run the following command:

`docker compose up`

The web-server will setup everything and connect itself to a postgis database, after which it will create the appropriate tables automatically. The server will listen for code changes, and restart itself thereafter (that is, you don't need to run this command after every change you make). If everything went right you see the output:

> `ais-web-1  | Starting development server at http://0.0.0.0:3000/`

Remember to recomment the line `python manage.py migrate --settings=local_settings` in the `entrypoint.sh` file.

## Accessing the local server

After setting up the AIS with Docker, you can access it in a web browser with the address "localhost:3000"

You will notice that there is no way to login to the system. This is because there are no users in the newly created, empty database. To solve this, you have to enter the Docker container and create a super user. To do this, (summarize process here)

First list the Docker processes using the command ```docker ps```. Find the process for the ais-web Docker container and note down the value in field "CONTAINER ID".

Then, you want to execute an interactive ```sh``` shell on the ais-web container, with the following command:

```docker exec -it containerid sh```

Where *containerid* is the container id of ais-web that you noted down. If done correctly, the command line prompt should now start with ```/usr/src/app #```.

From the shell in the countainer, execute the python script "manage.py" with the argument "createsuperuser"

```python manage.py createsuperuser```

You will then be prompted to enter a username, email, and password. After doing so, you can log in.



## Common issues

## Scripts

A number of scripts are available in the scripts folder. Others can be run with `manage.py [scriptname]`. Run `manage.py help` to list what scripts are available through manage.py

## License Information

Please check out [LICENSE.txt](LICENSE.txt) for information.
