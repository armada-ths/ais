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

## Accessing the local server

After setting up the AIS with Docker, you can access it in a web browser with the address `localhost:3000`

## Common issues

**Issue:** "I cannot log in to AIS!"

**Solution:** This is because there are no super users created in the system. Run `./init-dev-environment.sh` and enter the username and password for the super user. After doing this you can log into the AIS with these settings.

**Issue:** "I logged into my locally hosted AIS instance for the first time; but I can only see an error page!"

**Solution:** Most likely, you haven't created a fair yet. To do so, follow these steps:

1. Go to the admin page (`localhost:3000/admin/`)

2. Log in there again using your super user account, if needed.

3. On the admin page, find the "Fair" section, and press "Add" next to "Fairs" to add a new fair.

4. Now you need to fill out some information. Fill out the necessary fields (Registration start date & end date, Complete registration start date & end date). Make sure end dates come after start dates. Tick the "Current" box, and press save at the bottom of the page. The fair will be created, and you can go back to `localhost:3000` to see the landing page for the fair.

**Issue:** "entrypoint.sh not found"

**Solution:** If you're on Windows, you need to change the CRLF line endings in the file `entrypoint.sh` to LF line endings.

## Creating Database Migrations

When adding new fields to models, you will need to create a database migration. This migration will be performed on the server to update the database to the latest structure. After adding a field, and making sure the docker instance of AIS is up and running through docker compose, you run the following command:

```bash
./make-migrations <name of migration> <name of module where field was added>
```

## Scripts

A number of scripts are available in the scripts folder. Others can be run with `manage.py [scriptname]`. Run `manage.py help` to list what scripts are available through manage.py

## License Information

Please check out [LICENSE.txt](LICENSE.txt) for information.
