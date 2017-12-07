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
