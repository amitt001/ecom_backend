#!/bin/bash

printf "Running Setup....\n"

# Check for Debian or RHEL based system
YUM_CMD=$(which yum)
APT_GET_CMD=$(which apt-get)

if [ -n "$(command -v yum)" ]; then
    command=(command -c yum)
elif [ -n "$(command -v apt-get)" ]; then
    command=(command -v apt-get)
else
    echo "Not supported for this os"
    exit 1;
fi

# easy_install
easy_install --help >/dev/null 2>&1 && printf "Check easy_install: Done\n" || sudo command -y install python-setuptools
# pip
pip >/dev/null 2>&1 && printf "Check pip: Done\n" || sudo easy_install pip
# virtualenv
virtualenv > /dev/null  2>&1 && printf "Check virtualenv: Done\n"|| sudo -H pip install virtualenv

# create virtualenv
virtualenv env
# activate env
source env/bin/activate
# install required packages
pip install -r requirements.txt

printf "\nSetup complete\n"
printf "##############\n"

printf "\nMaking database migrations and applying them.\n"

pushd ecom_api && python manage.py makemigrations && python manage.py migrate && popd

# start app
printf "
Run tests:

    pushd ecom_api && ../env/bin/python manage.py test && popd

To run ecom_api:

    env/bin/python ecom_api/manage.py runserver
OR

    env/bin/gunicorn --pythonpath ecom_api ecom_api.wsgi --log-file -\n"

