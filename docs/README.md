# [AIS](http://ais.armada.nu/) — Armada Internal System

## Contribution Guides

See [CONTRIBUTING.md](CONTRIBUTING.md)

## Manual Development Setup

### Section 1: Installation of Dependencies

In order to run the project locally, you need the following tools:

#### [Docker](https://docs.docker.com/get-docker/) (used to run the server and database)

<details>
<summary>Windows</summary>

1. [Download Docker Desktop](https://docs.docker.com/desktop/install/windows-install/)

</details>

<details>
<summary>Orbstack with MacOS</summary>

1. [Download OrbStack](https://orbstack.dev/download)

</details>

#### [NVM](https://github.com/nvm-sh/nvm) (used to install Node)

<details>
<summary>Windows</summary>

1. `wsl`
2. `sudo apt-get install curl`
3. `curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/master/install.sh | bash`

</details>

<details>
<summary>MacOS with Homebrew</summary>

1. `brew install nvm`

</details>

#### [PNPM](https://pnpm.io/installation) (used to compile dashboard)

<details>
<summary>All platforms with NVM</summary>

1. `nvm install 20.12 && nvm use 20.12`
2. `npm install -g pnpm@9.6.0`

</details>

#### [Black](https://pypi.org/project/black/) (used to format code, **is not required to run the project**)

<details>
<summary>All platforms With PIP</summary>

1. `pip install black==23.3.0`

</details>

### Section 2: Setup of the Server

#### Prepare environment variables

1. `cp .env.example .env`

#### Prepare the production database copy

You can choose to use a copy of the production database for your local development.

1. Create a directory called `ais-developer-database` in the root directory.
2. Add the production database file (a file you get from HoIS) to that directory.
3. Rename the file `init.sql`.

#### Prepare static files

1. `nvm install 16 && nvm use 16 && npm install && npm run build` (compile the static files for e.g. the banquett and events systems).
2. `cd apps/dashboard` (goto dashboard project).
3. `nvm use 20.12 && pnpm install && pnpm build` (compile the the dashboard system).

#### Run the server

The server will run in a `docker compose` instance. To start the server, run the following command:

1. `docker compose up`

The web server will setup everything and connect itself to a postgis database. The server will listen for code changes, and restart itself thereafter (that is, you don't need to run this command after every change you make). If everything went right you see the output:

#### Migrate the database and create a super user

The database will not be up to date with the latest migrations. Run `./init-dev-environment.sh` to both migrate the database and to create a super user. The super user setup will guide you through giving the super user a name, email, and password. Enter whatever you feel is appropriate for your local development experience. If you only want to migrate the database, and not create a super user, simply exit the program using `ctrl+c` when it prompts you for the username for the super user. The server must be running in order to run this command.

> `ais-web-1  | Starting development server at http://0.0.0.0:3000/`

#### Accessing the local server

After setting up the AIS with Docker, you can access it in a web browser with the address `http://localhost:3000`

## Dashboard

### Development

The dashboard is where initial and final registration is made, as well as lunch tickets creation, exhibitor information, core values, logistics information, sture information. Development of this dashboard is done through in the folder `apps/dashboard`. Follow the instructions in the folder for starting the local React project. When running the React project, it will use `localhost:3000` as the URL for the backend, so you need to have AIS running in the background. The dashboard will be served the user `dashboard@armada.nu` in development mode, meaning you need to make sure this company contact exists. If you are e.g. doing final registration development, you need to make sure the company which this email belongs to is an exhibitor.

### Deployment

The dashboard is currently not being built in the automatic pipeline, meaning you need to build it yourself when deploying (TODO: add this to the automatic pipeline). Therefore, you need to run `pnpm build` in the `apps/dashboard` folder before merging into production.

## Common issues

<details>
<summary>I cannot log in to AIS!</summary>

This is because there are no super users created in the system. Run `./init-dev-environment.sh` and enter the username and password for the super user. After doing this you can log into the AIS with these settings.

</details>

<details>
<summary>I logged into my locally hosted AIS instance for the first time; but I can only see an error page!</summary>

Most likely, you haven't created a fair yet. To do so, follow these steps:

1. Go to the admin page (`localhost:3000/admin/`)

2. Log in there again using your super user account, if needed.

3. On the admin page, find the "Fair" section, and press "Add" next to "Fairs" to add a new fair.

4. Now you need to fill out some information. Fill out the necessary fields (Registration start date & end date, Complete registration start date & end date). Make sure end dates come after start dates. Tick the "Current" box, and press save at the bottom of the page. The fair will be created, and you can go back to `localhost:3000` to see the landing page for the fair.

</details>

<details>
<summary>entrypoint.sh not found</summary>

If you're on Windows, you need to change the CRLF line endings in the file `entrypoint.sh` to LF line endings.

</details>

<details>
<summary>'JSONError' object has no attribute 'get'</summary>

This error can occur when running the local version of the dashboard. In this case, it could mean that the development user for the dashboard does not exist. You need to create a company contact (for any company) with the email `dashboard@armada.nu`. The function `get_user` in `util/__init__.py` will use this user for all requests if you are in development mode.

</details>

## Creating Database Migrations

When adding new fields to models, you will need to create a database migration. This migration will be performed on the server to update the database to the latest structure. After adding a field, and making sure the docker instance of AIS is up and running through docker compose, you run the following command:

```bash
./make-migrations <name of migration> <name of module where field was added>
```

## Scripts

A number of scripts are available in the scripts folder. Others can be run with `manage.py [scriptname]`. Run `manage.py help` to list what scripts are available through manage.py

## License Information

Please check out [LICENSE.txt](LICENSE.txt) for information.
