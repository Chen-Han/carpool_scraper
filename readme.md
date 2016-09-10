

Overview
---
scapes page on UWCSSA 

We need a few things: 
1. a facebook app 
2. a server running in localhost:8000 accepting request
3. background scripting to scrape http://bbs.uwcssa.com/forum-54-1.html
4. ngrok that forwards request to localhost:8000

Please see https://abhaykashyap.com/blog/post/tutorial-how-build-facebook-messenger-bot-using-django-ngrok for a detailed guide on setting up a messenger app

Installation
----

Make sure `python -V` is 2.7 

```bash
# update all softwares
sudo apt-get upgrade && sudo apt-get update # might take a while
# mysql and unzip skip if installed
sudo apt-get install -y mysql-server unzip

# installing python dev, and other neccessary dependencies
sudo apt-get install -y lib32z1-dev libxml2-dev libxslt1-dev python-dev python-pip python-mysqldb

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

log into mysql database, create a database named scraper and change char set to utf-8
this is for chinese character compatibility
```sql
CREATE DATABASE scraper;
ALTER DATABASE scraper CHARACTER SET utf8 COLLATE utf8_general_ci;
```

*installing cronjob*

so that scraping runs in background
```bash
crontab -e
# add the following in prompted window, on the last line (without the #)
# also note that '~/scraper` is a sample path to the scraper directory, change as necessary
# 0,5,10,15,20,25,30,35,40,45,50,55 * * * * cd ~/scraper && python manage.py scrape_page
```

*starting server*
```bash
python manage.py migrate # applying migration
python manage.py runserver 
#open up a new bash session
ngrok http 8000

```

Configuring Facebook App
---
*It is highly recommended you read https://abhaykashyap.com/blog/post/tutorial-how-build-facebook-messenger-bot-using-django-ngrok first for pictorial guide*

* note the address that is forwarding request to localhost:8000 when running `ngrok` command, e.g. https://7f1ce852.ngrok.io
* now you will need to go to your ownfacebook app configuration e.g. https://developers.facebook.com/apps/1234-my-own-app/webhooks/ to set up the new webhook
* you will need to enter a `secret`, enter whatever, but make sure it matches `VERIFY_TOKEN` in `settings.ini`
* copy paste the app access token to `settings.ini` beside `ACCESS_TOKEN

`
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
# to set up the following, please see https://abhaykashyap.com/blog/post/tutorial-how-build-facebook-messenger-bot-using-django-ngrok in the token session
VERIFY_TOKEN: my-verify-token
ACCESS_TOKEN: my-token-here

```


