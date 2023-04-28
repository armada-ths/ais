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

#### Prepare the production database copy

You can choose to use a copy of the production database for your local development. Create a directory called `ais-developer-database.sql` in the root directory, and add the production database copy `init.sql` to it.

#### Run the server

The server will run in a `docker compose` instance. To start the server, run the following command:

`docker compose up`

The web-server will setup everything and connect itself to a postgis database. The server will listen for code changes, and restart itself thereafter (that is, you don't need to run this command after every change you make). If everything went right you see the output:

> `ais-web-1  | Starting development server at http://0.0.0.0:3000/`

#### Migrate the database and create a super user

The database will not be up to date with the latest migrations. Run `./init-dev-environment.sh` to both migrate the database and to create a super user. The super user setup will guide you through giving the super user a name, email, and password. Enter whatever you feel is appropriate for your local development experience. If you only want to migrate the database, and not create a super user, simply exit the program using `ctrl+c` when it prompts you for the username for the super user.

## Scripts

A number of scripts are available in the scripts folder. Others can be run with `manage.py [scriptname]`. Run `manage.py help` to list what scripts are available through manage.py

## License Information

Please check out [LICENSE.txt](LICENSE.txt) for information.
