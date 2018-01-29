targets = \
  help \
  \
  test \
  coverage \
  coverage-html \
  code-check \
  \
  update-schema \
  migration \
  migrate \
  models \
  \
  status \
  current \
  \
  run-server \
  stop-server \
  shutdown-vms \
  delete-vms \
  run-all-servers \
  stop-all-servers \
  shutdown-all-vms \
  delete-all-vms \
  \
  bash-shell \
  db-shell \
  django-shell \
  \
  load-db \
  dump-db \
  upload-db \
  clean-db-cache \
  \
  release-list \
  release \
  deploy \
  \
  update-packages \
  \
  build \


deprecated_targets = \
  bash \
  comp-message \
  coverage \
  coverage-run \
  coverage-report \
  coverage-html \
  coverage-html-open \
  load-remote-db \
  dev \
  fetch-remote-db \
  grant-permissions \
  lint \
  messages \
  nuke \
  restart \
  setup \
  shell \
  stop \
  superuser \


lower_target_help = \
  "build - Build (or rebuild) docker environment. Refreshes dependencies." \


target_help = \
  'help - Prints this help message.' \
  ' ' \
  'test - Run tests with no coverage. Run just those specified in $$(tests)' \
  '\tif provided.  E.g.:' \
  '\tmake test tests="impact.tests.test_file1 impact.tests.test_file2"' \
  'coverage - Run tests with coverage summary in terminal.' \
  'coverage-html - Run tests with coverage and open repot in browser.' \
  'code-check - Runs Flake8 and pep8 on the files changed between the' \
  '\tcurrent branch and $$(branch) (defaults to development)' \
  ' ' \
  'update-schema - Brings database schema up to date.  Specifically,' \
  '\tupdates any model definitions managed in other libraries,' \
  '\tcreates any needed migrations (uses $$(migration_name) if provided),' \
  '\truns any pending migrations.' \
  'migration - Create empty migration (uses $$(migration_name) if provided).' \
  'migrate - Runs any pending migrations.' \
  'models - Updates model definitions managed in other libraries.' \
  ' ' \
  'current - Switch all repos to development branch (or $$(branch)' \
  '\tif provided and available) and pulls down any changes to the branch.' \
  '\tReports any errors from the different repos.' \
  'status - Reports the status of all related source code repositories.' \
  ' ' \
  'run-server - Starts the local server.' \
  'stop-server - Stops the local server.' \
  'shutdown-vms - Shutdown local server VMs.' \
  'delete-vms - Deletes local server VMs an VM-related resources.' \
  'run-all-servers - Starts a set of related servers.' \
  'stop-all-server - Stops a set of related servers.' \
  'shutdown-all-vms - Shutdown set of related server VMs' \
  'delete-all-vms - Delets set of related server VMs' \
  ' ' \
  'bash-shell - Access to bash shell.' \
  'db-shell - Access to running database server.' \
  'django-shell - Access to Django shell.' \
  ' ' \
  'load-db - Load gzipped database file.' \
  '\tDefaults to db_cache/initial_schema.sql.gz.' \
  '\t$$(gz_file) can provide an explicit path.' \
  '\tOtherwise db_cache/$$(db_name).sql.gz is used.' \
  '\tIf no such file exists, then try download from S3.' \
  'clean-db-cache - Delete db_cache/initial_schema.sql.gz if it exists.' \
  'dump-db - Create a gzipped db dump.' \
  '\tDefaults to db_cache/initial_schema.sql.gz.' \
  '\t$$(gz_file) can provide an explicit path.' \
  '\tOtherwise db_cache/$$(db_name).sql.gz is used.' \
  'upload-db - Upload db dump to S3.' \
  '\tDefaults to uploading db_cache/initial_schema.sql.gz.' \
  '\t$$(db_name) defaults to initial_schema and sets the S3 key.' \
  '\t$$(gz_file) can provide an epxlicit path without changing the S3 key.' \
  ' ' \
  'release-list - List all releases that are ready to be deployed.' \
  'release - Create named release of releated servers.' \
  '\tRelease name is applied as a tag to all the related git repos.' \
  '\tRelease name defaults release-<version>.<number> where <version> is' \
  '\tthe first line of impact-api/VERSION and <number> is the next unused' \
  '\tnon-negative integer (0,1,2,...).' \
  '\t$$(release_name) overrides the entire release name.' \
  'deploy - Deploy $$(release_name) to a $$(target).' \
  '\tValid targets include "staging" (the default), "production",' \
  '\t "test-1", and "test-2"' \


grant_permissions_error_msg = PERMISSION_USER and PERMISSION_CLASSES must be \
  set.  E.g., 'make grant-permissions PERMISSION_USER=test@example.org PERMISSION_CLASSES=v0_clients'

RELEASE_EXAMPLE = E.g., 'make release DOCKER_REGISTRY=<ecr-container>.amazonaws.com ENVIRONMENT=staging AWS_SECRET_ACCESS_KEY=abcdefghijk AWS_ACCESS_KEY_ID=ABCDEFGH12IJKL'
registry_error_msg = DOCKER_REGISTRY must be set.  $(RELEASE_EXAMPLE)

awskey_error_msg  = AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY must be \
  set.  $(RELEASE_EXAMPLE)

environment_error_msg = ENVIRONMENT must be \
  set.  $(RELEASE_EXAMPLE)

no_release_error_msg = RELEASE must be set.  E.g., 'make deploy RELEASE=1.2.3.4'

.PHONY: $(targets) $(deprecated_targets)


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


# Testing, coverage, and code checking targets

tests ?= $(TESTS)  # Backwards compatibility
test: setup
	@docker-compose run --rm web \
		python3 manage.py test --configuration=Test $(tests)

coverage: coverage-run coverage-report coverage-html

coverage-run:
	@docker-compose run --rm web coverage run --omit="*/tests/*" --source='.' manage.py test --configuration=Test

coverage-report: DIFFBRANCH?=$(shell if [ "$(branch)" == "" ]; \
   then echo "development"; else echo "$(branch)"; fi;)
coverage-report: diff_files:=$(shell git diff --name-only $(DIFFBRANCH))
coverage-report: diff_sed:=$(shell echo $(diff_files)| sed s:web/impact/::g)
coverage-report: diff_grep:=$(shell echo $(diff_sed) | tr ' ' '\n' | grep \.py | grep -v /tests/ | grep -v /django_migrations/ | tr '\n' ' ' )
coverage-report:
	@docker-compose run --rm web coverage report --skip-covered $(diff_grep) | grep -v "NoSource:"

coverage-html:
	@docker-compose run --rm web coverage html --omit="*/tests/*"

coverage-html-open: coverage-html
	@open web/impact/htmlcov/index.html

branch ?= $(BRANCH)  # Backwards compatibility

code-check: DIFFBRANCH?=$(shell if [ "$(branch)" == "" ]; \
   then echo "development"; else echo "$(branch)"; fi;)
code-check:
	-@docker run --rm -v ${PWD}:/code -e BRANCH=$(DIFFBRANCH) \
		masschallenge/fpdiff /bin/bash | grep -v "^\.\/\.venv" | \
		grep -v "site-packages"


# Repos
REPOS = ../accelerate ../django-accelerator ../impact-api


# Database migration related targets
migrate:
	@docker-compose run --rm web ./manage.py migrate

ifdef MIGRATION_NAME
  MIGRATION_ARGS = --name $(MIGRATION_NAME)
endif
ifeq ($(EMPTY),1)
  MIGRATION_ARGS += --empty
endif

# migrations vs migration.  Should be run in django-accelerator.
# I don't think it should be run in impact-api.
migrations:
	@docker-compose run --rm web ./manage.py makemigrations $(MIGRATION_ARGS)



# Cross repo targets

status:
	@for r in $(REPOS) ; do \
	    echo ; echo Status of $$r; cd $$r; git status; done


# Server and Virtual Machine related targets
debug ?= 1

run-server: run-server-$(debug)

run-server-0:
	@docker-compose up

run-server-1:
	@docker-compose up -d
	@docker-compose exec web /bin/bash /usr/bin/start-nodaemon.sh

dev: run-server-0
runserver: run-server-1

stop-server:
	@docker-compose stop

shutdown-vms:
	@docker-compose down
	@rm -rf ./mysql/data
	@rm -rf ./redis

delete-vms: CONTAINERS?=$(shell docker ps -a -q)
delete-vms: IMAGES?=$(shell  docker images -q)
delete-vms:
	@docker rm -f $(CONTAINERS)
	@docker rmi -f $(IMAGES)


# Interactive shell Targets

bash-shell:
	@docker-compose exec web /bin/bash

db-shell:
	@docker-compose run --rm web ./manage.py dbshell

django-shell:
	@docker-compose run --rm web ./manage.py shell


# Database dump related targets

DB_CACHE_DIR = db_cache/
db_name ?= initial_schema
gz_file ?= $(DB_CACHE_DIR)$(db_name).sql.gz

load-db: $(DB_CACHE_DIR) $(gz_file)
	@echo "Loading $(gz_file)"
	@echo "drop database mc_dev; create database mc_dev;" | docker-compose run --rm web ./manage.py dbshell
	@gzcat $(gz_file) | docker-compose run --rm web ./manage.py dbshell
	@docker-compose run --rm web ./manage.py migrate

%.sql.gz:
	@echo downloading db...
	@wget -P ${dir $@} https://s3.amazonaws.com/public-clean-saved-db-states/$(notdir $@)

${DB_CACHE_DIR}:
	mkdir -p ${DB_CACHE_DIR}

clean-db-cache:
	@rm -rf $(gz_file)

dump-db:
	@docker-compose run --rm web /usr/bin/mysqldump -h mysql -u root -proot mc_dev | gzip > $(gz_file)
	@echo Created $(gz_file)

upload-db:
	@aws s3api put-object --acl public-read --bucket public-clean-saved-db-states --key $(db_name) --body $(gz_file)


TARGET ?= staging


deploy: DOCKER_REGISTRY = $(shell aws ecr describe-repositories | grep "repositoryArn" | awk -F':repository' '{print $1}' | awk -F'\"repositoryArn\":' '{print $2}')
deploy:
ifndef RELEASE
	$(error $(no_release_error_msg))
endif
	@ecs deploy --ignore-warnings $(TARGET) impact \
	--image web $(DOCKER_REGISTRY)/impact-api:$(RELEASE) \
	--image redis $(DOCKER_REGISTRY)/redis:$(RELEASE)

release: DOCKER_REGISTRY = $(shell aws ecr describe-repositories | grep "repositoryArn" | awk -F':repository' '{print $1}' | awk -F'\"repositoryArn\":' '{print $2}')
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
	@eval $(aws ecr get-login --region us-east-1);
	@ecs-cli configure --region us-east-1 --access-key $(AWS_ACCESS_KEY_ID) --secret-key $(AWS_SECRET_ACCESS_KEY) --cluster $(ENVIRONMENT);
	@docker tag impactapi_web:latest $(DOCKER_REGISTRY)/impact-api:$(IMAGE_TAG)
	@docker push $(DOCKER_REGISTRY)/impact-api:$(IMAGE_TAG)
	@docker tag impactapi_redis:latest $(DOCKER_REGISTRY)/redis:$(IMAGE_TAG)
	@docker push $(DOCKER_REGISTRY)/redis:$(IMAGE_TAG)
	@ecs-cli compose -f docker-compose.prod.yml down
	@ecs-cli compose -f docker-compose.prod.yml up



# Deprecated targets

dbdump:
	@echo ERROR: dbdump has been replaced by dump-db

dbload:
	@echo ERROR: dbload has been replaced by load-db

dbshell:
	@echo ERROR: dbshell has been replaced by db-shell


comp-messages:
	@docker-compose exec web python manage.py compilemessages

messages:
	@docker-compose exec web python manage.py makemessages -a

lint:
	@docker-compose run --rm web pylint impact
