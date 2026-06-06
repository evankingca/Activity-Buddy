# cst8268-group-project

Gymbros / Golfbros

## Install

You'll need:

- [Python](https://www.python.org/downloads/)
- [Postgresql](https://www.postgresql.org/download/)

Once you have python installed, it's probably best to create a virtual environment. In the project's root folder, run:

```
python -m venv .\cst8268
```

```
.\.venv\Scripts\activate
```

Then install all the pip dependencies, including Django:

```
python -m pip install -r .\requirements.txt
python manage.py tailwind install
```

Then, to start the dev server:

```
python manage.py tailwind dev
```

This essentially just runs `python manage.py runserver` along with starting the tailwind watcher. You can read more about all that [here](https://django-tailwind.readthedocs.io/en/latest/)
