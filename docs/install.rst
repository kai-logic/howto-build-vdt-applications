============
Installation
============

Pre-Requisites
==============

* `setuptools <http://pypi.python.org/pypi/setuptools>`_
* `virtualenv <http://pypi.python.org/pypi/virtualenv>`_

For everything to run smoothly you'll need Python 3, Node and Yarn (or NPM) installed.

Python and PIP
==============

For Linux
=========

Installing::

    apt-get install software-properties-common python-software-properties
    apt-get update
    apt-get install python3.5
    python3.5 -V

Upgrade pip, setuptools and weel::

    sudo pip3 install --upgrade pip setuptools wheel

For OSX
=======

First install Homebrew (https://brew.sh/index_se.html) ::

    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Then run the following, this will install the latest version of python 3 and pip automatically::

    brew install python3

To install Node and Yarn please refer to their respective site for instructions::

    https://nodejs.org/en/download/
    https://yarnpkg.com/lang/en/docs/install/

Developers on Ubuntu, install yarn as such::

    sudo npm install -g yarnpkg

or::

    curl -o- -L https://yarnpkg.com/install.sh | bash

If yarn -v shows incorrect version, you have to open a new terminal window.

Installing
==========

Stand in the root of app for all the following

Django, creating a virtualenv for Python 3::

    python3 -m venv ~/.virtualenv/app

And then activate it::

    source ~/.virtualenv/app/bin/activate

Once active, python3 and pip3 will be default, so you can run the normal::

    python [command]
    pip [command]

Python packages, to install Django and other dependecies run::

    pip install -r requirements.pip

Run Development Servers
=======================

Django
First you will have to create a `local.py` file to point to the Vidispine server you are using::

    touch app/settings/local.py

Add the following settings in the `local.py` file (Vidispine might not be locally installed)::

    from .dev import *
    VSAPI_BASE = 'http://localhost:8080/API/'

With the virutalenv still active (see above) run::

    yarn build
    python manage.py collectstatic
    python manage.py runserver 127.0.0.1:8000 --settings=app.settings.local


Backend Development
===================

If you are developing the VSUI Django backend, you should use either IntelliJ or PyCharm as IDE.

Always start the server in debug mode in the IDE and use breakpoints instead of printing things in
the console.

In your IDE, open `File->Settings...` and search for `Project interpreter`, click the cog and add
`~/.virtualenv/app/bin/python3.5`.

In your IDE, open `File->Settings...` and search for `Python interpreter`, select `Python 3.5 ...`

Create a server config with following settings::

    Script: ... /app/manage.py
    Script-parameters: runserver --settings=app.settings.local
    Python-interpreter: Project default 3.5...

Building Documentation
======================

Documentation is available in ``docs`` and can be built into a number of
formats using `Sphinx <http://pypi.python.org/pypi/Sphinx>`_. To get started::

    pip install Sphinx
    cd docs
    make html

This creates the documentation in HTML format at ``docs/_build/html``, open in your favorite
browser::

    <browser> path-to/vdt/your-project/docs/_build/html/index.html
