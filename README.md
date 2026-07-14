# cst8268-group-project

Gymbros / Golfbros project.

## Install

Before starting, you'll need:

- [Python](https://www.python.org/downloads/)
- [Postgresql](https://www.postgresql.org/download/)
- [Node.JS](https://nodejs.org/en/download) (If you have Laravel Herd installed on your system, it should already be installed. Check by running `node --version`)

Since we're using Django 6, you'll need at least Python 3.12. Check with `python --version`

### Setup

Once you have Python installed, it's probably best to create a virtual environment. In the project's root folder, run:

```
python -m venv .venv
```

> Note: If you have multiple versions of python on your machine and it defaults to one older than 3.12, you'll need to force it to use the newer version: `python3.14 -m venv .venv`

Then, if you're on Windows:

```
.\.venv\Scripts\activate
```

Or if you're on Mac/Linux:

```
source ./.venv/bin/activate
```

### Install

Install all the pip dependencies, including Django:

```
python -m pip install -r requirements.txt
```

And then install tailwind and it's deps:

```
python manage.py tailwind install
```

Once you've done that you'll need to create a `.env` file, which is where we'll store all the credentials for connecting to the database. I've create a file called `.env.template` which you can copy and then rename to `.env`. If you've on Windows and set up Postgres using all the defaults, you shouldn't have to edit anything in here. If you're on Mac though and installed through brew, your default postgres username will be to set to your Mac's user account name, so you'll need to update the file with that.

To run the migration, you'll first need to create a table called `gymgolf`. To do that, you'll need to log into Postgres via the command line using `psql`. If you're on Windows, it should be something like:

```
psql -U postgres -d postgres
```

On Mac, it'll be:

```
psql -U yourMacUsername -d postgres
```

Once you have a postgres prompt, you can run:

```
create database gymgolf;
```

Once that's set up, you should `exit` out of the postgres prompt and run this to test the connection and set up the required tables:

```
python manage.py migrate
```

### Run

Then finally, to start the dev server with the Tailwind watcher on Windows, you'll need two terminals open. In one terminal, run:

```
python manage.py tailwind start
```

...and in the other, run:

```
python manage.py runserver
```

If you're not doing any front-end stuff, you can use just the `runserver` one.

On Mac/Linux, it's just one command:

```
python manage.py tailwind dev
```

Which essentially just runs `python manage.py runserver` along with starting the tailwind watcher. You can read more about how that works [here](https://django-tailwind.readthedocs.io/en/latest/)

Then just go to [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the site.

### Troubleshooting

If your on Windows and you run into an issue where Tailwind tells you:

```
CommandError:
It looks like node.js and/or npm is not installed or cannot be found.
```

you'll need to uncomment the line for configuring `NPM_BIN_PATH` in your `.env` file. Make sure it's set to the actual location of NPM on your system.

---

Have fun!

\- Shoppature Team
