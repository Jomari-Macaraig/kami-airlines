# KAMI AIRLINES

## Setting up development

### 1. Cloning the project.
```commandline
$ git clone <repo-url> kami_airlines
$ cd kami_airlines
```

### 2. Create virtualenv (go to your virtualenv folder if you have)
```commandline
virtualenv <virtual_env_name>
```

### 3. Install requirement/dependencies
```commandline
$ pip install -r requirements/development.txt
```
For testing, install test.txt
```commandline
$ pip install -r requirements/test.txt
```

### 4.Set environment variables.
Please see env.template for environment variables to be configured for the project.  
Don't use the previous environment variables, replace it with
```commandline
$ export DJANGO_SETTINGS_MODULE='config.settings.development'
$ export DJANGO_SECRET_KEY='testing123'
```

### 5. Run migration.
```commandline
$ python manage.py migrate
```

### 6. Spin-up a development server.
```commandline
$ python manage.py runserver
```

### 7. Visit browsable API page to play around with the API
- /api/v1/airplanes

## Testing
### Running test
```commandline
$ python manage.py test
```
### Running coverage
```commandline
$ coverage run manage.py test
$ coverage html --omit="admin.py"
```

### TODO
1. Use Docker
2. Use PostgreSQL
