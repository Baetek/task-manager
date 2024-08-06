.PHONY: run-locally seed-local-db build-docker install-local-depts

# Load repo .env file
ifneq (,$(wildcard ./.env))
    include .env
    export $(shell sed 's/=.*//' .env)
endif

IS_VENV := $(shell if [ -z "$$VIRTUAL_ENV" ]; then echo "false"; else echo "true"; fi)

#   ______   ____  ____    ____    ___ ______  _____
#  |      | /    ||    \  /    |  /  _]      |/ ___/
#  |      ||  o  ||  D  )|   __| /  [_|      (   \_ 
#  |_|  |_||     ||    / |  |  ||    _]_|  |_|\__  |
#    |  |  |  _  ||    \ |  |_ ||   [_  |  |  /  \ |
#    |  |  |  |  ||  .  \|     ||     | |  |  \    |
#    |__|  |__|__||__|\_||___,_||_____| |__|   \___|
#                                                   

run-locally: assert-venv-exists seed-local-db install-local-depts
	@echo "Running locally..."
	pip install -r requirements.txt
	uvicorn app.main:app --port ${EXTERNAL_PORT} --reload

run-in-cluster:
	docker compose --env-file .env up --build 

test: assert-venv-exists seed-local-db install-local-depts
	pytest -s app/tests/

black:
	black app/*.py

#   __ __    ___  _      ____   ___  ____    _____
#  |  |  |  /  _]| |    |    \ /  _]|    \  / ___/
#  |  |  | /  [_ | |    |  o  )  [_ |  D  )(   \_ 
#  |  _  ||    _]| |___ |   _/    _]|    /  \__  |
#  |  |  ||   [_ |     ||  | |   [_ |    \  /  \ |
#  |  |  ||     ||     ||  | |     ||  .  \ \    |
#  |__|__||_____||_____||__| |_____||__|\_|  \___|
#        

# Build API image
build-docker:
	docker build \
		--build-arg PYTHON_VERSION=${PYTHON_VERSION} \
		--build-arg EXTERNAL_PORT=${EXTERNAL_PORT} \
		--tag task-manager .

assert-venv-exists:
ifeq ($(IS_VENV), true)
	@echo "Virtual environment is active."
else
	@echo "Not running inside a Python virtual environment.\
	       When running locally we expect that you have sourced / activated a Python venv"
	@exit 1
endif

seed-local-db:
	@echo "Seeding the local database..."
	# Add your commands to seed the local database here

install-local-depts:
	pip install -r requirements.txt
