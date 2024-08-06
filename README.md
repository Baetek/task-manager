### To hiring manager notes

Please bear with me, 

```
Python 3.9 and 3.10 support ✅
Correctly apply code formatting, preferably using the Black format ✅
Apply type annotations ✅ (in most places, not super happy that it's complete)
Use of a light weight framework ✅
Tasks must be stored in a database ✅
Database must be managed by code using migrations ✅
```

Unfortunately I have chewed off more than I could handle and decided to try get a full prod type setup going with 
mysql, redis caching of endpoints, all under docker-compose. To show off. Along with configuration of every run-mode via an .env file

I don't know what I was thinking because all of this together is definitely more than a 1 day job. 

you can still try it with `make run-in-cluster`, the real mysql database is not being populated for me for some reason even though I've verified DB_RESET_ON_START=True in that envrionment. 

You can verify switching python version via .env file when using the cluster, Docker will put in the python version specified.

Suffered as a result of trying to show off too much:

```
Code cleanliness ❌ it's a bit messy, not fully documented etc - THIS IS WHAT I SHOULD HAVE FOCUSED ON
Alembic migration test ❌ the only failing test is the alembic test
```

## Getting Started

The easiest way to get started is to copy `.env.template` to `.env`
and use `make run-in-cluster` to run as a docker-compose cluster or 
`make run-locally` if you are running in a Python venv
or `make test` to run tests

## Config

Your .env file allows you to set most configurable items for all supported run modes.

## Documentation & Test UI

Available at `/docs` of the app, via Swagger, e.g `localhost:5000/docs`

## Supported Run Configurations

The supported run configurations are:
1. Prod (For a fake prod setup I am using docker-compose to spin up a real mysql and redis server) - *Supports changing python version between 3.9 and 3.10 via .env file.*
2. Local (For local setup I am just using pip and venv with a file on disk database)
3. Testing (For testing I am using pytest with an in-memory database) 

These are all supported via the Makefile

I wanted to show off Docker and spend time on that, but in reality the better way to support differing Python versions for all run modes would be to use Poetry, specifying the python version in `pyproject.toml`. As I say I am demonstrating a docker setup instead.

![supported-run-configurations-prod](docs/images/supported-run-configurations-prod.png)

![supported-run-configurations-local](docs/images/supported-run-configurations-local.png)

![supported-run-configurations-pytest](docs/images/supported-run-configurations-pytest.png)
