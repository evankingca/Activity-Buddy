# Activity Buddy

Activity Buddy project, started in summer 2026 by Morp Machine. Built in Django 6 with a Postgres DB, Tailwind on the frontend and Django REST framework on the backend. Previously used temp name Gymbros / Golfbros.

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

## Troubleshooting

### NPM Not Installed Error

If your on Windows and you run into an issue where Tailwind tells you:

```
CommandError:
It looks like node.js and/or npm is not installed or cannot be found.
```

you'll need to uncomment the line for configuring `NPM_BIN_PATH` in your `.env` file. Make sure it's set to the actual location of NPM on your system.

### Conflicts with tailwindApp/static/css/dist/styles.css

Tailwind works by reading all your HTML files and compiling a
custom stylesheet based on the Tailwind classes you've used in
them. Normally, a tool like Vite would handle this at runtime,
but since Django works differently, this file actually gets
built by `tailwind dev` or `start` and included into git. This
can lead to lots of conflicts on that file when trying to
merge changes. Since it's an auto-generated file though, it
doesn't really matter how you resolve them. Production should
always rebuild this file before deploying anyway, so you
shouldn't have to worry about things getting broken. So
basically don't worry about it, it doesn't really matter how
you fix the conflicts, it will get rebuilt anyway.

## Some useful info

This is some info about the development practices we used. It's best to follow these to keep things consistent.

### CSS & Tailwind

Although we mostly use Tailwind for styling, sometimes you're
writing a set of classes so often it makes sense to have them
be reusable. Tailwind is more built for a framework like React
that has a robust component system, but unfortunately Django's
is quite primitive. So instead, we write utility and component
classes in `tailwindApp/static_src/src/styles.css`. Usually
when possible, we try to use Tailwind's built-in functions for
handling stuff. See
[here](https://tailwindcss.com/docs/adding-custom-styles#adding-component-classes)
for some of the options available.

When writing classes for elements, you should write it such
that you have a base class (e.g. `btn`) that is variant-agnostic,
with child classes (e.g. `btn-primary`, `btn-sm`) that modify
properties of that base class. The base class should be in the
components layer (`@layer components { .btn {...} }`) to allow
for easy overrides, while child classes should be utilities
(`@utility btn-primary {...}`) so they can be used with variants
(e.g. `class="card card-primary dark:card-secondary"`)

When writing dark and light variants of elements, separate each
variant into their own utilities, and then apply the to main
utility via:

```
@apply element-light dark:element-dark
```

This allows you to force either the dark or light variant by
simply overriding the element's default variant for that
respective colour scheme. For example, to force an input to
always be dark, you could do:

```
class="link link-dark"
```

To force it to light mode, you would override the dark variant:

```
class="link dark:link-light"
```

It's sometimes also a good idea to do this for padding variants.

Since elements are written as base and child classes, they
should be applied like bootstrap classes. e.g. If you want
your button to be a primary one, you would apply:

```
class="btn btn-primary"
```

A small Secondary button would be:

```
class="btn btn-sm btn-secondary"
```

---

Have fun!

\- Morp
