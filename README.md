# cove-oc4ids

## Dev installation

```bash
git clone https://github.com/open-contracting/cove-oc4ids.git
cd cove-oc4ids
virtualenv .ve --python=/usr/bin/python3
source .ve/bin/activate
pip install -r requirements_dev.txt
python manage.py migrate
python manage.py compilemessages
python manage.py runserver
```

You may need to pass `0.0.0.0:8000` to `runserver` in the last step, depending on your development environment.

Note: requires `gettext` to be installed. This should come by default with Ubuntu, but just in case:

```bash
sudo apt update
sudo apt install gettext
```

## Building the stylesheets

```bash
pysassc -t compressed -I bootstrap cove_ocds/sass/styles-oc4ids.sass cove_ocds/static/dataexplore/css/bootstrap-oc4ids.css
```

## Running the tests

```bash
pytest
```

## Command-line interface

[lib-cove-oc4ids](https://github.com/open-contracting/lib-cove-oc4ids) offers a command-line interface for validating OC4IDS data.
