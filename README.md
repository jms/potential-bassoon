# potential-bassoon [![Build Status](https://travis-ci.org/jms/potential-bassoon.svg?branch=master)](https://travis-ci.org/jms/potential-bassoon)

### Setup instructions

Requirements:
- Python 3
- PostgreSQL
- virtualenvwrapper(optional for development)

```bash
# local development
git clone https://github.com/jms/potential-bassoon.git 
cd potential-bassoon
mkvirtualenv -p /usr/bin/python3  venv 
pip install -r requirements.txt

# setup the database, replace the connection string using the env.sample file
# as reference
cp env.sample .env

# run the migrations
./manage.py migrate  # or python manage.py migrate

# create the fake users
./manage.py create_fake_users 100

# for verbose output
# ./manage.py create_fake_users -v2 100

# running the application
./manage.py runserver  # or just run make

# go to  http://localhost:8000
```
Application running on Heroku for demo purpose:

https://fast-woodland-88106.herokuapp.com/

