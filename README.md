# cst8268-group-project

Gymbros / Golfbros project.

## Install

Before starting, you'll need:

- [Python](https://www.python.org/downloads/)
- [Postgresql](https://www.postgresql.org/download/)

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

Once you've done that you'll need to create a `.env` file, which is where we'll store all the credentials for connecting to the database. I've create a file called `.env.template` which you can copy and then rename to `.env`. If you've set up Postgres using all the defaults, you shouldn't have to edit anything in here. But if your accessing it with a custom user or you're hosting on a separate machine, you'll need to change some values in the file.

Once that's set up, you should run this to test the connection and set up the required tables:

```
python manage.py migrate
```

### Run

Then finally, to start the dev server:

```
python manage.py tailwind dev
```

Which essentially just runs `python manage.py runserver` along with starting the tailwind watcher. You can read more about how that works [here](https://django-tailwind.readthedocs.io/en/latest/)

Then just go to [http://127.0.0.1:8000](http://127.0.0.1:8000) to see the site.

Have fun!

\- Shoppature Team
