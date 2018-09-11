# Vidispine Content Viewer
A content viewer for inpecting the Vidispine API

## Getting Started
These instructions will get you a copy of the project up and running on your local machine for 
development and testing purposes. See deployment for notes on how to deploy the project on a live 
system.

For everything to run smoothly you'll need Python 3, Node and Yarn (or NPM) installed.

### Python
#### Using MacOS:
```
1. Install Homebrew (https://brew.sh/index_se.html)
2. brew install python3
```

#### Using Linux:
Installing
```
apt-get install software-properties-common python-software-properties
apt-get update
apt-get install python3.5
python3.5 -V
```

Upgrade pip, setuptools and wheel:
```
sudo pip3 install --upgrade pip setuptools wheel
```

### Node and Yarn
#### MacOS:
`brew install yarn` 

#### Linux
Refer to:
* [node.js](https://nodejs.org/en/download/)
* [yarnpkg.com](https://yarnpkg.com/lang/en/docs/install/)

### Installing

Stand in the root of vidispine_cv for all the following

#### Django

##### Creating a virtualenv for Python 3:

```
python3 -m venv ~/.virtualenv/vidispine_cv
```

And then activate it:
```
source ~/.virtualenv/vidispine_cv/bin/activate
```

Once active, python3 and pip3 will be default, so you can run the normal
```
python [command]
pip [command]
```

#### Python packages
To install Django and other dependencies run
```
pip install -r requirements.pip
```

#### Vue + Front-end packages

Vidispine Content Viewer is running a bunch of packaged from NPM, install them with yarn:
```
yarn install
```

### Run Development Servers

#### Django
First you will have to create a `local.py` file to point to the Vidispine server you are using:
```
touch vidispine_cv/settings/local.py
```

Add the following settings in the `local.py` file:
Important note: Vidispine might not be locally installed, use the ip to your Vidispine instance.
```
from .dev import *
VSAPI_BASE = 'http://localhost:8080/API/'
```

Vidispine CV is using the Vidispine-Python-SDK, install it:
```
python3 -m pip install -e git+https://github.com/vidispine/temp-vdt-python-sdk.git#egg=vdt-python-sdk
```
(use `... install -U -e ...` in order to update it)

With the virutalenv still active (see above) run:
```
yarn build
python manage.py runserver 127.0.0.1:8000 --settings=vidispine_cv.settings.local
```

#### Vue.js
We're using Poi (https://poi.js.org) to build the app and serve a development server, this enables
hot-reload and automatic transpilation/bundling. For the development server to work with the Django API we need to proxy the
Poi-dev-server to the Django-server.

Create `poi.dev.config.js` in the root and add the following to it:

```
// Proxy servers becoause of CORS,
// Browsers does not allow cross origin XHR:s!
module.exports = {
  devServer: {
    proxy: {
      '/api/**': {
        target: 'http://localhost:8000',
        secure: false,
      },
      '/apinoauth/**': {
        target: 'http://localhost:8080',
        secure: false,
        pathRewrite: {
          '^/apinoauth': '/APInoauth',
        },
      },
    },
  },
};

```

Where the target is the IP-address you Django-server is running on.

Then simply run to run development server.
```
yarn start
```

If you open your browser with the IP printed in your terminal you should now see a working version
of Vidispine UI!

#### Visual Studio Code
We strongly recommend using [Visual Studio Code](https://code.visualstudio.com/) with the [Vetur Plugin](https://marketplace.visualstudio.com/items?itemName=octref.vetur) for the best experience while working with Vue. Follow [this eslintguide](https://vuejs.github.io/vetur/setup.html#eslint) for correct eslint config.

## Backend Development
While developing the Django backend, we at Vidispine prefer to use IntelliJ or PyCharm as IDE.

> Even if you're not using one of the mentioned IDE's, selecting the correct Python 3 interpreter will make your life easier!

Always start the server in debug mode in the IDE and use breakpoints instead of printing things in 
the console.

In your IDE, open `File->Settings...` and search for `Project interpreter`, click the cog and add 
`~/.virtualenv/vidispine_cv/bin/python3.5`.
 
In your IDE, open `File->Settings...` and search for `Python interpreter`, select `Python 3.5 ...`

Create a server config with following settings:
```
Script: ... /app/manage.py
Script-parameters: runserver --settings=app.settings.local
Python-interpreter: Project default 3.5...
```

## Deployment
We use docker to build and reploy the application

### Build Docker image

    $ docker build -t vidispine/cv .
    $ docker run -ti -e VIDISPINE_IP_PORT=http://34.241.228.200:8080 -e HTTPS=false -p8000:80 vidispine/cv

### Acknowledgments
This package couldn't have been made without the awesome work made by:
* [Vue.js](https://github.com/vuejs/) 
* [Django](https://github.com/django/)

... and a lot of other great Open Source projects that can be seen in package.json 