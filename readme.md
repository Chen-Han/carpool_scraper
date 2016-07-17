

Overview
---
scapes page on UWCSSA 


Installation
----

Make sure `python -V` is 2.7 

```
# update all softwares
sudo apt-get upgrade && sudo apt-get update # might take a while
# mysql, skip if installed
sudo apt-get install mysql-server
# installing python dev, and other neccessary dependencies for xml parsing
sudo apt-get install lib32z1-dev libxml2-dev libxslt1-dev python-dev
# neccessary dependencies for app
sudo apt-get install python-mysqldb
# install ngrok, for development
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip
cp ngrok /usr/bin/ngrok # so that we can use ngrok on command line
# download this project, cd to the project root
# set settings.ini for tokens 
touch settings.ini
# see below for a sample settings.ini file
# finally install all application dependencies
pip install -r requirements.txt
```

log into mysql database, change char set to utf-8
this is for chinese character compatibility
```
ALTER DATABASE scraper CHARACTER SET utf8 COLLATE utf8_general_ci;
```

*installing cronjob*
```
0,5,10,15,20,25,30,35,40,45,50,55 * * * * cd ~/scraper && python manage.py scrape_page
```

Sample settings.ini
----

```
[database]
DATABASE_USER: my-user
DATABASE_PASSWORD: my-password
DATABASE_HOST: localhost
DATABASE_PORT: 3306
DATABASE_ENGINE: mysql
DATABASE_NAME: scraper
TESTSUITE_DATABASE_NAME: test_scraper

[secrets]
SECRET_KEY: random-ascii-string
CSRF_MIDDLEWARE_SECRET: random-ascii-string

[cookies]
SESSION_COOKIE_DOMAIN:

# all settings in debug section should be false inproductive
# environment
# INTERNAL_IPS should be empty in productive environment

[debug]
DEBUG: true
TEMPLATE_DEBUG: true
VIEW_TEST: true
INTERNAL_IPS: 127.0.0.1
SKIP_CSRF_MIDDLEWARE: true

[email]
SERVER_EMAIL: django@localhost
EMAIL_HOST: localhost

# the [error mail] and [404 mail] sections are special. Just add
# lines with
#  full name: email_address@domain.xx
# each section must be present but may be empty.
[error mail]
Adam Smith: adam@localhost

[404 mail]
John Wayne: john@localhost

[tokens]
VERIFY_TOKEN: my-verify-token
ACCESS_TOKEN: my-token-here

```


