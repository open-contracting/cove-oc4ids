# cove-oc4ids

### Caching

In non-dev or (not DEBUG mode) the default settings make use of a local memcached server. This backend requires a local memcached server running. On debian based systems this can be installed with `sudo apt install memcached`.

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

[Set up chromedriver](https://chromedriver.chromium.org/getting-started), then run:

```bash
pytest
```

## Translations

We use Django's translation framework to provide this application in different languages.
We have used Google Translate to perform initial translations from English, but expect those translations to be worked on by humans over time.

### Translations for Translators

Translators can provide translations for this application by becomming a collaborator on Transifex https://www.transifex.com/open-contracting-partnership-1/cove-1/

### Translations for Developers

For more information about Django's translation framework, see https://docs.djangoproject.com/en/1.8/topics/i18n/translation/

If you add new text to the interface, ensure to wrap it in the relevant gettext blocks/functions.

In order to generate messages and post them on Transifex:

First check the `Transifex lock <https://opendataservices.plan.io/projects/co-op/wiki/CoVE_Transifex_lock>`, because only one branch can be translated on Transifex at a time.

Then:

```bash
python manage.py makemessages -l en
tx push -s
```

In order to fetch messages from transifex:

```bash
tx pull -a
```

In order to compile them:

```bash
python manage.py compilemessages
```

Keep the makemessages and pull messages steps in thier own commits seperate from the text changes.

To check that all new text is written so that it is able to be translated you could install and run `django-template-i18n-lint`

```bash
pip install django-template-i18n-lint
django-template-i18n-lint cove
```

## Command-line interface

[lib-cove-oc4ids](https://github.com/open-contracting/lib-cove-oc4ids) offers a command-line interface for validating OC4IDS data.
