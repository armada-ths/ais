import { $ } from "bun";
import chalk from "chalk";
import { spawn } from "child_process";
import commandExists from "command-exists";
import fs from "fs";

async function pause() {
  console.log("Press any ENTER to continue...");

  for await (const _ of console) {
    return;
  }
}

function folderExist(path: string) {
  return fs.existsSync(path);
}

async function notInstalled(command: string) {
  try {
    const exists = await commandExists(command);

    if (exists) {
      console.log(chalk.green(`✅ ${command} is installed`));
      return false;
    }
    return true;
  } catch (error) {
    return true;
  }
}

console.log(chalk.blue("Installing dependencies..."));
if (await notInstalled("nvm")) {
  console.log(chalk.yellow("\nNVM is not installed"));
  console.log(chalk.blue("Install NVM from the following links:"));
  console.log(
    chalk.blue(
      chalk.bold("Windows:"),
      "https://github.com/coreybutler/nvm-windows"
    )
  );
  console.log(
    chalk.blue(
      chalk.bold("Mac:"),
      "https://github.com/nvm-sh/nvm?tab=readme-ov-file#installing-and-updating"
    )
  );
  await pause();
}

if (await notInstalled("node")) {
  console.log(chalk.yellow("\nNode is not installed"));
  console.log(chalk.blue("Run: ", chalk.bold("nvm install 16")));
  pause();
}

// Check node version
const nodeVersion = await $`node --version`.text();
const [major] = nodeVersion.slice(1).split(".").map(Number);
if (major != 16) {
  console.log(chalk.blue("Your current version is", nodeVersion));
  console.log(chalk.yellow("\nNode version is not 16"));
  console.log(
    chalk.blue(
      "Run:",
      chalk.bold("nvm install 16 && nvm use 16"),
      "in the root directory"
    )
  );
  await pause();
} else {
  console.log(chalk.green("✅ Node version is 16"));
}

if (await notInstalled("pnpm")) {
  await $`npm install -g pnpm`.text();
  console.log(chalk.green("Installed pnpm"));
}

if (await notInstalled("docker")) {
  console.log(chalk.yellow("Docker is not installed"));
  console.log(
    "Download Docker Desktop from the following links:",
    chalk.blue(
      chalk.bold("Windows:"),
      "https://docs.docker.com/desktop/windows/install/"
    )
  );
  console.log(
    chalk.blue(
      chalk.bold("Mac:"),
      "https://docs.docker.com/desktop/mac/install/"
    )
  );
  await pause();
}

console.log(chalk.green(chalk.bold("Dependencies installed!\n")));

if (!(await Bun.file("../.env").exists())) {
  console.log(chalk.blue("Copying .env.example file..."));
  await $`cp .env.example .env`.cwd("../").text();
} else {
  console.log(chalk.green("✅ .env file set up!"));
}

// Check if folder exists
if (!folderExist("../ais-developer-database.sql")) {
  await $`mkdir ais-developer-database.sql`.cwd("../");
}
if (!(await Bun.file("../ais-developer-database.sql/init.sql").exists())) {
  console.log(
    chalk.blue(
      "You can choose to use a copy of the production database for your local development. In the root directory, and add the production database copy `init.sql` to it."
    )
  );
  await pause();
}
console.log(chalk.blue("Installing node dependencies..."));
await $`npm install && npm run build`.cwd("../").text();
console.log(chalk.green("✅ Banquet system dependencies installed"));
await $`pnpm install`.cwd("../apps/dashboard").text();
console.log(chalk.green("✅ Dashboard system dependencies installed"));

console.log(chalk.blue("Make sure that you have Docker running!"));
console.log(
  chalk.blue(
    chalk.italic(
      "It is running if you have the docker desktop application open"
    )
  )
);
await pause();

console.log(chalk.blue("Starting the development server..."));
console.log(await $`docker compose up --detach`.cwd("../").text());
console.log(chalk.green("✅ Development server started"));

console.log(
  chalk.blue(`
Lastly we will run the script ./init-dev-environment.sh to set up the database and seed it with data.
This script performs two tasks:
1. Perform database migrations
2. Creates a root user 
${chalk.italic(
  "if you already have a root user configured, you can safely exit this script with Ctrl+C"
)}
`)
);
await pause();

const shell = spawn("../init-dev-environment.sh", [], { stdio: "inherit" });
await new Promise((resolve) => shell.on("close", resolve));
console.log(
  chalk.green(`
✅ Database setup complete!
You should now be able to access the application at http://localhost:3000`)
);
