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

## Creating Database Migrations

When adding new fields to models, you will need to create a database migration. This migration will be ran on the server to update the database to the latest structure. After adding a field, you run the following command:

```bash
python3 manage.py makemigrations --name <name of migration> <name of module where field was added> --settings=ais.local.settings
```

Running this command will attempt to migrate your local database, specified by the settings in `ais.local.settings`. Since the development environment is ran in a docker-compose instance, you will not have access to a local database, making the above command fail. To counteract this, you can temporarily switch out the database engine, specific in `ais.local.settings`, to a dummy database, by switching out the `ENGINE` variable to `django.db.backends.dummy`.

## Scripts

A number of scripts are available in the scripts folder. Others can be run with `manage.py [scriptname]`. Run `manage.py help` to list what scripts are available through manage.py

## License Information

Please check out [LICENSE.txt](LICENSE.txt) for information.
