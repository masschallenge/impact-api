targets = \
  help \
  \
  test \
  coverage \
  coverage-html \
  code-check \
  \
  update-schema \
  data-migration \
  migrations \
  migrate \
  \
  status \
  checkout \
  \
  run-server \
  stop-server \
  shutdown-vms \
  delete-vms \
  build \
  run-all-servers \
  stop-all-servers \
  shutdown-all-vms \
  delete-all-vms \
  build-all \
  \
  bash-shell \
  db-shell \
  django-shell \
  \
  load-db \
  load-remote-db \
  dump-db \
  upload-db \
  clean-db-cache \
  \
  release-list \
  deploy \

deprecated_targets = \
  bash \
  comp-message \
  coverage \
  coverage-run \
  coverage-report \
  coverage-html \
  coverage-html-open \
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


DEFAULT_DB_NAME = initial_schema
db_name ?= $(DEFAULT_DB_NAME)

lower_target_help = \


target_help = \
  'help - Prints this help message.' \
  ' ' \
  'test - Run tests with no coverage and while preserving the test database.' \
	'\tIf you do not want to preserve the database add the keepdb=no flag E.g. make test keepdb=no' \
	'\tRun just those specified in $$(tests)' \
  '\tmake test tests="impact.tests.test_file1 impact.tests.test_file2"' \
  'coverage - Run tests with coverage summary in terminal.' \
  'coverage-html - Run tests with coverage and open report in browser.' \
  'code-check - Runs Flake8 and pycodestyle on the files changed between the' \
  '\tcurrent branch and $$(branch) (defaults to $(DEFAULT_BRANCH))' \
  ' ' \
  'update-schema - Brings database schema up to date.  Specifically,' \
  '\tupdates any model definitions managed in other libraries,' \
  '\tcreates any needed migrations (uses $$(migration_name) if provided),' \
  '\truns any pending migrations.' \
  'data-migration - Create empty migration.' \
  '\tUses $$(migration_name) if provided.' \
  'migrations - Create any needed auto-generated migrations.' \
  '\tUses $$(migration_name) if provided.' \
  'migrate - Runs migrations. If $$(migration) is given then then that ' \
  '\tmigration is targeted in the accelerator package unless another ' \
  '\t$$(application) is given.  Examples:' \
  '\taccelerate 0123: make migrate migration=0123' \
  '\tsimpleuser 0123: make migrate migration=0123 application=simpleuser' \
  ' ' \
  'status - Reports the status of all related source code repositories.' \
  'checkout - Switch all repos to $(DEFAULT_BRANCH) branch (or $$(branch)' \
  '\tif provided and available) and pulls down any changes to the branch.' \
  '\tReports any errors from the different repos.' \
  ' ' \
  'run-server - Starts the local server. Set debug=0 for supervisor output.' \
  '\t When running the server for the first time after a build, the database' \
  '\t specified by $$(gz_file) will be loaded.' \
  ' ' \
  'stop-server - Stops the local server.' \
  'shutdown-vms - Shutdown local server VMs.' \
  'delete-vms - Deletes local server containers. In order to delete Docker ' \
  '\t images, run `make delete-vms remove_images=`, and related images will ' \
  '\t be pruned.' \
  ' ' \
  'build - Build (or rebuild) docker environment. Refreshes dependencies.' \
  'run-all-servers - Starts a set of related servers.' \
  'stop-all-server - Stops a set of related servers.' \
  'shutdown-all-vms - Shutdown set of related server VMs' \
  'delete-all-vms - Deletes set of related server VMs' \
  'build-all - Builds dependencies for set of related servers' \
  ' ' \
  'bash-shell - Access to bash shell.' \
  'db-shell - Access to running database server.' \
  'django-shell - Access to Django shell.' \
  ' ' \
  '-- Database targets --' \
  'Database targets use the make variables db_name and gz_file.' \
  'db_name defaults to $(DEFAULT_DB_NAME)' \
  'gz_file defaults to db_cache/$$(db_name).sql.gz' \
  ' ' \
  'load-db - Load gzipped database file.' \
  '\tIf $S$(gz_file) does not exist, then try to download from S3' \
  '\tusing the key "$$(db_name).sql.gz".' \
  'clean-db-cache - Delete $$(gz_file) if it exists.' \
  'load-remote-db - Delete $$(gz_file) if it exists, then run load-db.' \
  'dump-db - Create a gzipped db dump.' \
  '\tCreates db_cache/$$(db_name).sql.gz.' \
  '\tNote that dump-db ignores $$(gz_file).' \
  'upload-db - Upload db dump to S3.' \
  '\tS3 key is always $$(db_name).sql.gz' \
  '\tUploads $$(gz_file) and make it publicly accessible. The command uses' \
  'the AWS KEY and SECRET specified in .dev.env, make sure they are ' \
  'configured with a user who has upload permissions prior to execution.' \
  ' ' \
  'release-list - List all releases that are ready to be deployed.' \
  'deploy - Deploy $$(release_name) to a $$(target).' \
  '\tValid targets include "staging" (the default), "production",' \
  '\t "test-1", and "test-2"' \

# Repos
ACCELERATE = ../accelerate
API_APP = ../accelerate/mcproject/api
DJANGO_ACCELERATOR = ../django-accelerator
IMPACT_API = ../impact-api
FRONT_END = ../front-end
SEMANTIC = ../semantic-ui-theme
REPOS = $(ACCELERATE) $(DJANGO_ACCELERATOR) $(FRONT_END) $(SEMANTIC) $(IMPACT_API) $(API_APP)
FRONTEND_MAKE = cd $(FRONT_END) && $(MAKE)

.PHONY: $(targets) $(deprecated_targets)


.env:
	@touch .env

help:
	@echo "Valid targets are:\n"
	@for t in $(target_help) ; do \
	    echo $$t; done
	@echo

setup: .env
	@cp git-hooks/pre-commit .git/hooks/pre-commit
	@cp git-hooks/prepare-commit-msg .git/hooks/prepare-commit-msg
	@mkdir -p ./mysql/data
	@mkdir -p ./redis

ACCELERATE_VERSION:=$(shell git describe --tags --abbrev=0)
build: shutdown-vms delete-vms setup
	@docker build -f Dockerfile.fpdiff -t masschallenge/fpdiff .
	@docker-compose build --build-arg ACCELERATE_VERSION=$(ACCELERATE_VERSION)

# Testing, coverage, and code checking targets

tests ?= $(TESTS)  # Backwards compatibility
test: setup
	@@if [ -z $$keepdb ]; then keepdb="--keepdb"; else keepdb=""; fi; \
	docker-compose run --rm web \
		python3 -Wa manage.py test $$keepdb --configuration=Test $(tests)

export FRONTEND_PATH := $(shell ./external_abs_path.sh $(FRONT_END))
coverage: coverage-run coverage-report coverage-html-report

coverage-run: .env
	@docker-compose run --rm web coverage run --omit="*/tests/*" --source='.' manage.py test --configuration=Test

coverage-report: diff_files:=$(shell git diff --name-only $(branch))
coverage-report: diff_sed:=$(shell echo $(diff_files)| sed s:web/impact/::g)
coverage-report: diff_grep:=$(shell echo $(diff_sed) | tr ' ' '\n' | grep \.py | grep -v /tests/ | grep -v /django_migrations/ | tr '\n' ' ' )
coverage-report: .env
	@docker-compose run --rm web coverage report -i --skip-covered $(diff_grep) | grep -v "NoSource:"

coverage-html-report: .env
	@docker-compose run --rm web coverage html --omit="*/tests/*"

coverage-xml-report: .env
	@docker-compose run --rm web coverage xml -i  --omit="*/tests/*"

coverage-html: coverage
	@open web/impact/htmlcov/index.html

DEFAULT_BRANCH = development
branch ?= $(DEFAULT_BRANCH)
ifdef BRANCH
  branch = $(BRANCH)  # Backwards compatibility
endif

code-check:
	-@docker run --rm -v ${PWD}:/code -e BRANCH=$(branch) \
		masschallenge/fpdiff /bin/bash | grep -v "^\.\/\.venv" | \
		grep -v "site-packages"



# Database migration related targets

data-migration migrations: .env
	@cd $(DJANGO_ACCELERATOR) && $(MAKE) $@ \
	  migration_name=$(migration_name) | \
	  sed "s|accelerator/|$(DJANGO_ACCELERATOR)/accelerator/|" | \
	  sed "s|simpleuser/|$(DJANGO_ACCELERATOR)/simpleuser/|"


application ?= accelerator

MIGRATE_CMD = docker-compose run --rm web ./manage.py migrate $(application) $(migration)
migrate: .env
	@$(MIGRATE_CMD)

update-schema: migrations
	@$(MIGRATE_CMD)

# Cross repo targets

status:
	@for r in $(REPOS) ; do \
	    echo ; echo Status of $$r; cd $$r; \
	    git -c 'color.ui=always' status | sed "s|^|$$r: |"; done

checkout:
	@for r in $(REPOS) ; do \
		cd $$r; \
		git fetch 2>/dev/null; \
		if [ $$? -ne 0 ]; then \
			echo "Fetching the latest from the remote failed, you may not be able to checkout an existing remote branch."; \
			echo "Check your internet connection if the checkout fails."; \
			echo ""; \
		fi; \
		git branch -a | egrep $(branch) > /dev/null; \
		if [ $$? -eq 0 ]; then \
			git -c 'color.ui=always' checkout $(branch) > /tmp/gitoutput 2>&1; \
		else \
			echo "$(branch) doesn't exist, checking out $(DEFAULT_BRANCH)..."; \
			git -c 'color.ui=always' checkout $(DEFAULT_BRANCH) > /tmp/gitoutput 2>&1; \
		fi; \
		{ cat /tmp/gitoutput & git pull; } | sed "s|^|$$r: |"; \
		echo; \
	done

watch-frontend stop-frontend: process-exists=$(shell ps -ef | egrep -h "./watch_frontend.sh|parcel watch" | grep -v "grep" | awk '{print $$2}')
watch-frontend:
	@if [ -z "$(process-exists)" ]; then \
		cd $(FRONT_END) && nohup bash -c "./watch_frontend.sh &" && cd $(IMPACT_API); \
	fi;

stop-frontend:
	@if [ -n "$(process-exists)" ]; then \
		kill $(process-exists); \
	fi;


# Server and Virtual Machine related targets
debug ?= 1

set-frontend-version:
	@$(FRONTEND_MAKE) get-version

run-server: set-frontend-version run-server-$(debug)

run-server-0: .env initial-db-setup watch-frontend ensure-mysql
	@docker-compose up

run-detached-server: .env initial-db-setup watch-frontend ensure-mysql set-frontend-version
	@docker-compose up -d
	@docker-compose run --rm web /usr/bin/mysqlwait.sh

run-server-1: run-detached-server watch-frontend ensure-mysql
	@docker-compose exec web /bin/bash /usr/bin/start-nodaemon.sh

dev: run-server-0
runserver: run-server-1


initial-db-setup: CONTAINER_CREATED:=$(shell docker ps -a -q --filter ancestor=mysql --filter network=impactapi_default)
initial-db-setup:
	@if [ -z "$(CONTAINER_CREATED)" ]; then \
		rm -f ./mysql_entrypoint/0002*; \
		cp $(gz_file) ./mysql_entrypoint/0002_$(notdir $(gz_file)); \
	fi;

stop-server: .env stop-frontend
	@docker-compose stop

shutdown-vms: .env stop-frontend
	@docker-compose down
	@rm -rf ./redis

REMOVE_IMAGES = no
remove_images ?= $(REMOVE_IMAGES)
delete-vms: CONTAINERS?=$(shell docker ps -a -q --filter name=^/impact-api)
delete-vms: .env
	@echo "Removing impact-api images and containers"
	@echo "This may take a while if you have a lot of unused images"
	@echo "Containers....."
	@echo $(shell if [ ! -z "$(CONTAINERS)" ]; then docker rm -f $(CONTAINERS); fi;)
	@echo "Images....."
	@echo $(shell if [ -z "$(remove_images)" ]; then docker image prune -a -f; fi;)

ACCELERATE_MAKE = cd $(ACCELERATE) && $(MAKE)

run-all-servers: run-detached-server
	@$(ACCELERATE_MAKE) run-detached-server

stop-all-servers: stop-server
	@$(ACCELERATE_MAKE) stop-server

shutdown-all-vms: shutdown-vms
	@$(ACCELERATE_MAKE) shutdown-vms

delete-all-vms: delete-vms
	@$(ACCELERATE_MAKE) delete-vms

build-all: build
	@$(ACCELERATE_MAKE) build

# Interactive shell Targets

bash-shell: .env ensure-mysql
	@docker-compose exec web /bin/bash || docker-compose run --rm web /bin/bash

db-shell: .env ensure-mysql
	@docker-compose run --rm web ./manage.py dbshell

django-shell: .env ensure-mysql
	@docker-compose run --rm web ./manage.py shell


# Database dump related targets

DB_CACHE_DIR = db_cache/
s3_key = $(db_name).sql.gz
gz_file ?= $(DB_CACHE_DIR)$(s3_key)
intermediary_file = /tmp/sql_dump.sql

load-db: $(DB_CACHE_DIR) $(gz_file) .env ensure-mysql
	@echo "Loading $(gz_file)"
	@echo "This will take a while, don't be alarmed if your console appears frozen."
	@echo "drop database mc_dev; create database mc_dev; use mc_dev;" > $(intermediary_file)
	@gzcat $(gz_file) >> $(intermediary_file)
	@sed -i "" "s|\`masschallenge\`|\`mc_dev\`|g" $(intermediary_file)
	@cat $(intermediary_file) | docker-compose run --rm web ./manage.py dbshell
	@rm -rf $(intermediary_file)
	@docker-compose run --rm web ./manage.py migrate --noinput

%.sql.gz:
	@echo downloading db...
	@wget -P ${dir $@} https://s3.amazonaws.com/public-clean-saved-db-states/$(notdir $@)

${DB_CACHE_DIR}:
	mkdir -p ${DB_CACHE_DIR}

clean-db-cache:
	@rm -f $(gz_file)

load-remote-db: clean-db-cache
	$(MAKE) load-db gz_file=$(gz_file)

mysql-container: run-detached-server

dump-db: mysql-container
	@echo Creating a new dump for $(DB_CACHE_DIR)$(s3_key)
	@docker-compose run --rm web /usr/bin/mysqldump -h mysql -u root -proot mc_dev -r /$(DB_CACHE_DIR)$(db_name).sql
	@rm -f $(DB_CACHE_DIR)$(s3_key)
	@gzip $(DB_CACHE_DIR)$(db_name).sql
	@echo Created $(DB_CACHE_DIR)$(s3_key)

MAX_UPLOAD_SIZE = 160000000

upload-db: build-aws
	@if [ `wc -c < $(gz_file) | tr -d '[:space:]'` -gt $(MAX_UPLOAD_SIZE) ]; \
	then \
	  echo \\nError: Dump file exceeds $(MAX_UPLOAD_SIZE) bytes.; \
	  echo This may indicate that this dump contains sensitive data \\n; \
	else \
	  echo Uploading $(gz_file) as $(s3_key); \
	  read -r -p "Are you sure? [y/N] " response; \
	  if [[ "$$response" =~ ^([yY][eE][sS]|[yY])+$$ ]]; \
	  then \
	    echo Uploading $(gz_file) as $(s3_key)...; \
		docker run -v $$PWD/$(gz_file):/data/$(notdir $(gz_file)) --rm  \
		--env-file .dev.env \
		masschallenge/aws \
		aws s3 cp $(notdir $(gz_file)) \
		s3://public-clean-saved-db-states/$(s3_key) --acl public-read; \
	  else \
	    echo Cancelled upload successfully.; \
	  fi \
	fi

build-aws:
	docker build -f Dockerfile.aws db_cache/ -t masschallenge/aws:latest


TARGET ?= staging


release release-list:
	@$(ACCELERATE_MAKE) $@


travis-release: DOCKER_REGISTRY = $(shell aws ecr describe-repositories | grep "repositoryArn" | awk -F':repository' '{print $1}' | awk -F'\"repositoryArn\":' '{print $2}')
travis-release:
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
	@export ECR_TOKEN=`aws ecr get-authorization-token --region us-east-1 --output text --query 'authorizationData[].authorizationToken' | base64 --decode | cut -d':' -f2`; \
	export ECR_HOST=`aws ecr get-authorization-token --region us-east-1 --output text --query 'authorizationData[].proxyEndpoint'`; \
	export DOCKER_USER=AWS; \
	export DOCKER_PASSWORD=$$ECR_TOKEN; \
	echo $$DOCKER_PASSWORD | docker login -u $$DOCKER_USER --password-stdin $$ECR_HOST;
	@ecs-cli configure profile travis --access-key $(AWS_ACCESS_KEY_ID) --secret-key $(AWS_SECRET_ACCESS_KEY);
	@ecs-cli configure --region us-east-1 --cluster $(ENVIRONMENT);
	@docker tag impactapi_web:latest $(DOCKER_REGISTRY)/impact-api:$(IMAGE_TAG)
	@docker push $(DOCKER_REGISTRY)/impact-api:$(IMAGE_TAG)
	@docker tag impactapi_redis:latest $(DOCKER_REGISTRY)/redis:$(IMAGE_TAG)
	@docker push $(DOCKER_REGISTRY)/redis:$(IMAGE_TAG)
	@ecs-cli compose -f docker-compose.prod.yml down
	@ecs-cli compose -f docker-compose.prod.yml up


deploy:
	@if [ "$$TRAVIS_PULL_REQUEST" != "false" ] || [ "$$IMAGE_TAG" != "development" ]; then exit 1; fi;
	@pip install --upgrade certifi pyopenssl requests[security] ndg-httpsclient pyasn1 pip botocore
	@curl -s https://raw.githubusercontent.com/silinternational/ecs-deploy/master/ecs-deploy | sudo tee /usr/bin/ecs-deploy
	@sudo chmod +x /usr/bin/ecs-deploy
	@ecs-deploy -c $$PRE_STAGING_ECS_CLUSTER -n $$PRE_STAGING_ECS_SERVICE -i $$DOCKER_REGISTRY/impact-api:$$IMAGE_TAG --force-new-deployment

# Deprecated targets
dbdump:
	@echo ERROR: dbdump has been replaced by dump-db

dbload:
	@echo ERROR: dbload has been replaced by load-db

dbshell:
	@echo ERROR: dbshell has been replaced by db-shell


comp-messages: .env
	@docker-compose exec web python manage.py compilemessages

messages: .env
	@docker-compose exec web python manage.py makemessages -a

lint: .env ensure-mysql
	@docker-compose run --rm web pylint impact

ensure-mysql: kill-exited-containers
	@$(ACCELERATE_MAKE) ensure-mysql

kill-exited-containers: containers-to-kill=$(shell docker ps -a -q --filter status=exited --filter name=impact)
kill-exited-containers:
	-@if [ -n "$(containers-to-kill)" ]; then \
		echo "Removing unused impact docker containers..."; \
		docker rm -f $(containers-to-kill); \
		echo "Done removing containers."; \
	fi;
