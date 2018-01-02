IMAGE_TAG = $(shell git rev-parse --abbrev-ref HEAD)
DOCKER_REGISTRY = $(shell aws ecr describe-repositories | grep "repositoryArn" | awk -F':repository' '{print $1}' | awk -F'\"repositoryArn\":' '{print $2}')

targets = \
  bash \
  build \
  clean \
  code-check \
  comp-message \
  coverage \
  coverage-run \
  coverage-report \
  coverage-html \
  coverage-html-open \
  dump-db \
  load-db \
  load-remote-db \
  db-shell \
  deploy \
  dev \
  fetch-remote-db \
  grant-permissions \
  help \
  lint \
  messages \
  nuke \
  release \
  restart \
  setup \
  shell \
  stop \
  superuser \
  test \


deprecated_targets = \
  demo \


target_help = \
  "bash - Shell access to webserver (web container)." \
  "build - Build (or rebuild) docker environment. Refreshes dependencies." \
  "clean - Shutdown all running containers and removes data files." \
  "code-check - Runs Flake8 and pep8 on the files changed between the current branch and and a given BRANCH (defaults to development)" \
  "comp-message - Compiles .po files and makes them available to Django." \
  "coverage - Run coverage and generate text report." \
  "coverage-html - Run coverage and generate HTML report." \
  "dump-db - Create a gzipped database dump as dump.sql.gz in local directory." \
  "load-db - Load gzipped database file. GZ_FILE must be defined." \
  "db-shell - Access to running MySQL." \
  "dev - Start all containers needed to run a webserver." \
  "fetch-remote-db - Updates a DB image from remote container." \
  "grant-permissions - Grants PERMISSION_CLASSES to PERMISSION_USER." \
  "help - Prints this help message." \
  "lint - Runs any configured linters (pylint at the moment)." \
  "load-remote-db - fetches a remote db and loads it in one target." \
  "messages - Creates .po files for languages targeted for translation." \
  "nuke - The nuclear option. Deletes ALL images and containers." \
  "release - pushes to a given DOCKER_REGISTRY with the provided AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY" \
  "restart - Restart webserver processes. Necessary after code changes." \
  "shell - Access to Django shell." \
  "stop - Stops all docker containers." \
  "superuser - Creates a superuser account in the Django process." \
  "test - Run tests. To run a single test:" \
  "\tmake test TESTS='impact.tests.test_api_routes.TestApiRoute.test_api_object_get impact.tests.test_api_routes.TestApiRoute.test_api_object_delete'"


load_db_error_msg = GZ_FILE must be set. \
  E.g. 'make load-db GZ_FILE=${DB_CACHE_DIR}initial_schema.sql.gz'

fetch_remote_db_error_msg = DB_FILE_NAME must be set. \
  E.g. 'make $(MAKECMDGOALS) DB_FILE_NAME=initial_schema.sql.gz' or

grant_permissions_error_msg = PERMISSION_USER and PERMISSION_CLASSES must be \
  set.  E.g., 'make grant-permissions PERMISSION_USER=test@example.org PERMISSION_CLASSES=v0_clients'

registry_error_msg = DOCKER_REGISTRY must be \
  set.  E.g., 'make release DOCKER_REGISTRY=<ecr-container>.amazonaws.com ENVIRONMENT=staging AWS_SECRET_ACCESS_KEY=abcdefghijk AWS_ACCESS_KEY_ID=ABCDEFGH12IJKL'

awskey_error_msg  = AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be \
  set.  E.g., 'make release DOCKER_REGISTRY=<ecr-container>.amazonaws.com ENVIRONMENT=staging AWS_SECRET_ACCESS_KEY=abcdefghijk AWS_ACCESS_KEY_ID=ABCDEFGH12IJKL'

environment_error_msg = ENVIRONMENT must be \
  set.  E.g., 'make release DOCKER_REGISTRY=<ecr-container>.amazonaws.com ENVIRONMENT=staging AWS_SECRET_ACCESS_KEY=xGDsdAsdEGS AWS_ACCESS_KEY_ID=ABCDTSDS43DXAS'


.PHONY: $(targets) $(deprecated_targets)

DB_CACHE_DIR = db_cache/

help:
	@echo "Valid targets are:\n"
	@for t in $(target_help) ; do \
	    echo $$t; done
	@echo

setup:
	@cp git-hooks/pre-commit .git/hooks/pre-commit
	@cp git-hooks/prepare-commit-msg .git/hooks/prepare-commit-msg
	@mkdir -p ./mysql/data
	@mkdir -p ./redis

build: clean setup
	@docker build -f fpdiff.Dockerfile -t masschallenge/fpdiff .
	@docker-compose build --no-cache

superuser:
	@docker-compose run --rm web ./manage.py createsuperuser

code-check: DIFFBRANCH?=$(shell if [ "${BRANCH}" == "" ]; \
   then echo "development"; else echo "${BRANCH}"; fi;)
code-check:
	-@docker run --rm -v ${PWD}:/code -e BRANCH=$(DIFFBRANCH) \
		masschallenge/fpdiff /bin/bash | grep -v "^\.\/\.venv" | \
		grep -v "site-packages"

# you may get timeouts here occasionally
# see https://github.com/docker-library/docs/tree/master/mysql#no-connections-until-mysql-init-completes
dev:
	@docker-compose up

test: setup
	@docker-compose run --rm web \
		python3 manage.py test --configuration=Test $(TESTS)

bash:
	@docker-compose exec web /bin/bash

runserver:
	@docker-compose exec web /bin/bash /usr/bin/start-nodaemon.sh

shell:
	@docker-compose run --rm web ./manage.py shell

db-shell:
	@docker-compose run --rm web ./manage.py dbshell

stop:
	@docker-compose stop

nuke: CONTAINERS?=$(shell docker ps -a -q)
nuke: IMAGES?=$(shell  docker images -q)
nuke:
	@docker rm -f $(CONTAINERS)
	@docker rmi -f $(IMAGES)

clean:
	@docker-compose down
	@rm -rf ./mysql/data
	@rm -rf ./redis

comp-messages:
	@docker-compose exec web python manage.py compilemessages

coverage: coverage-run coverage-report coverage-html

coverage-run:
	@docker-compose run --rm web coverage run --omit="*/tests/*" --source='.' manage.py test --configuration=Test

coverage-report: DIFFBRANCH?=$(shell if [ "${BRANCH}" == "" ]; \
   then echo "development"; else echo "${BRANCH}"; fi;)
coverage-report: diff_files:=$(shell git diff --name-only $(DIFFBRANCH))
coverage-report: diff_sed:=$(shell echo $(diff_files)| sed s:web/impact/::g)
coverage-report: diff_grep:=$(shell echo $(diff_sed) | tr ' ' '\n' | grep \.py | grep -v /tests/ | grep -v /django_migrations/ | tr '\n' ' ' )
coverage-report:
	@docker-compose run --rm web coverage report --skip-covered $(diff_grep) | grep -v "NoSource:"

coverage-html:
	@docker-compose run --rm web coverage html --omit="*/tests/*"

coverage-html-open: coverage-html
	@open web/impact/htmlcov/index.html

demo:
	@docker-compose run --rm web ./manage.py make_demo_users
	@docker-compose run --rm web ./manage.py make_demo_apps

lint:
	@docker-compose run --rm web pylint impact

messages:
	@docker-compose exec web python manage.py makemessages -a

dump-db:
	@docker-compose run --rm web /usr/bin/mysqldump -h mysql -u root -proot mc_dev | gzip > dump.sql.gz
	@echo Created dump.sql.gz

GZ_FILE ?= $(DB_CACHE_DIR)$(DB_FILE_NAME)

load-db:
ifeq ($(GZ_FILE), $(DB_CACHE_DIR))
	$(error $(load_db_error_msg))
endif
	@echo "drop database mc_dev; create database mc_dev;" | docker-compose run --rm web ./manage.py dbshell
	@gzcat $(GZ_FILE) | docker-compose run --rm web ./manage.py dbshell
	@docker-compose run --rm web ./manage.py migrate --no-input

${DB_CACHE_DIR}:
	mkdir -p ${DB_CACHE_DIR}

fetch-remote-db: ${DB_CACHE_DIR}
fetch-remote-db:
ifndef DB_FILE_NAME
	$(error $(fetch_remote_db_error_msg))
endif
	@echo cleaning cache for ${DB_FILE_NAME}
	@rm -f ${DB_CACHE_DIR}$(DB_FILE_NAME)
	@echo downloading db...
	@wget -P ${DB_CACHE_DIR} https://s3.amazonaws.com/public-clean-saved-db-states/${DB_FILE_NAME}

load-remote-db: fetch-remote-db load-db


restart:
	@docker-compose restart web

grant-permissions:
ifndef PERMISSION_CLASSES
	$(error $(grant_permissions_error_msg))
endif
	@docker-compose run --rm web ./manage.py grant_permissions $(PERMISSION_USER) $(PERMISSION_CLASSES)

deploy: IMAGE_TAG?=$(shell if [ "${RELEASE_TAG}" == "" ]; then echo "${IMAGE_TAG}"; else echo "${RELEASE_TAG}"; fi;)
deploy:
	@ecs deploy --ignore-warnings $(ENVIRONMENT) impact --image web $(DOCKER_REGISTRY)/impact-api:$(IMAGE_TAG) --image redis $(DOCKER_REGISTRY)/redis:$(IMAGE_TAG)

release: IMAGE_TAG?=$(shell if [ "${RELEASE_TAG}" == "" ]; then echo "${IMAGE_TAG}"; else echo "${RELEASE_TAG}"; fi;)
release:
ifndef AWS_SECRET_ACCESS_KEY
	$(error $(awskey_error_msg))
endif
ifndef AWS_ACCESS_KEY_ID
	$(error $(awskey_error_msg))
endif
ifndef ENVIRONMENT
	$(error $(environment_error_msg))
endif
	@echo "tagging image ${IMAGE_TAG}"
	@echo $AWS_ACCESS_KEY_ID
	@eval $(aws ecr get-login --region us-east-1);
	@ecs-cli configure --region us-east-1 --access-key $(AWS_ACCESS_KEY_ID) --secret-key $(AWS_SECRET_ACCESS_KEY) --cluster $(ENVIRONMENT);
	@docker tag impactapi_web:latest $(DOCKER_REGISTRY)/impact-api:$(IMAGE_TAG)
	@docker push $(DOCKER_REGISTRY)/impact-api:$(IMAGE_TAG)
	@docker tag impactapi_redis:latest $(DOCKER_REGISTRY)/redis:$(IMAGE_TAG)
	@docker push $(DOCKER_REGISTRY)/redis:$(IMAGE_TAG)
	@ecs-cli compose -f docker-compose.prod.yml down
	@ecs-cli compose -f docker-compose.prod.yml up

dbdump:
	@echo ERROR: dbdump has been replaced by db-dump

dbload:
	@echo ERROR: dbload has been replaced by load-db

dbshell:
	@echo ERROR: dbshell has been replaced by db-shell
