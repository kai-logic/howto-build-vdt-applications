#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
ORANGE='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

#Check if virutal env is active
if [[ "$VIRTUAL_ENV" != "" ]]
then
  pip install -r requirements.pip
  pip install -e git+https://github.com/vidispine/temp-vdt-python-sdk.git#egg=vdt-python-sdk
  yarn install
  yarn build
  read -p "Enter Vidispine URL (https://example.myvidispine.com): " URL
  read -p "Enter Vidispine username: " username
  read -sp "Enter Vidispine password: " password
  printf "from .dev import *\n
VSAPI_BASE = \'$URL/API/\'
VS_USERNAME = \'${username}\'
VS_PASSWORD =  \'${password}\'
" > ./app/settings/local.py
  
  printf "${BLUE}app/settings/local.py created${NC}\n"
  read -p "Create dev-server config? (Y/n): " devServer
  if [ ${devServer} != "n" ]
  then
    printf "module.exports = {
  devServer: {
    proxy: {
      '/api/**': {
        target: 'http://localhost:8000',
        secure: false
      },
      '/apinoauth/**': {
        target: \'$URL\',
        secure: false,
        pathRewrite: { 
          '^/apinoauth': '/APInoauth'
        },
      },
    }
  }
}" > ./poi.dev.config.js
  printf "${BLUE}poi.dev.config.js created with proxy localhost:8000. Be sure to change your port if your're running Django on port 8000${NC}\n"
  fi
  printf "${GREEN}Complete${NC}\n"
  printf "Run ${ORANGE}./manage.py runserver 127.0.0.1:8000 --settings=app.settings.local${NC} to start Django server\n"
  printf "Run ${ORANGE}'yarn start'${NC} to start development server\n"
  printf "Run ${ORANGE}'yarn build'${NC} to build you app for production\n"
else
    echo "Virtual environment not active. Activate it before running setup..."
fi
