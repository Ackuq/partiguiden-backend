# partiguiden-backend

**THIS REPOSITORY HAS BEEN DEPRECATED, ITS FUNCTIONALITY HAS BEEN MOVED TO https://github.com/ackuq/partiguiden**

### Setup

1. Copy the `.env.example` configuration file and rename it `.env.dev`. Fill the missing configuration values with the ones provided by your project leader:

```sh
cp .env.example .env.dev
```

2. Start the application:

```sh
docker-compose up
```

2. Setup the app database:

```sh
docker-compose exec web pipenv run ./manage.py migrate
```

3. Create an admin user for the Django Admin (the credentials are up to you):

```sh
docker-compose exec web pipenv run ./manage.py createsuperuser
```
