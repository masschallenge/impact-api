_MIT License_
_Copyright (c) 2017 MassChallenge, Inc._

# Impact API Server


 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
 ![Travis](https://img.shields.io/travis/masschallenge/impact-api.svg)
<a href="https://codeclimate.com/github/masschallenge/impact-api/maintainability">
  <img src="https://api.codeclimate.com/v1/badges/919b52c7bf78bfc67bb6/maintainability" />
</a>
 

## Quickstart

1. Install [Docker](https://docs.docker.com/docker-for-mac/)
   (download the stable channel).
2. Start Docker from the Applications folder.
3. Build the project.

    ``` git
    git clone https://github.com/masschallenge/impact-api.git
    cd impact-api/
    make dev
    ```

4. Once the process completes (it will take a few minutes), visit
http://127.0.0.1:8000 in a browser.

5. Shutdown and cleanup.

    ``` git
    make clean
    ```

## Commands

This section describes the commands you may need when developing the
website.

### Create a superuser

    make superuser

### Rebuilding the container

This should be done whenever the requirements change or `INSTALLED_APPS`
is changed.

Can be done with:

    make build
    
Note that this command will reset the DB, so any changes you've made
before (i.e. `make dbload`, `make superuser`...) should be
re-executed.


### Creating a release:

To create a release run the ```make release``` command which will tag your current HEAD
with a semantic release tag and also tag the related django-accelerator and accelerate repos.

run:
    make release

Upon tagging the release, a new commit will be created and pushed with the release tag.
This will trigger a new travis build (and subsequently a new tagged ECR image)

### Reloading on Code change:

This should be done whenever the code changes. Otherwise the changes
won't be reflected in the website.

Can be done with:

    make reload

## Using Makefile Commands

The `Makefile` in the root of the project provides a number of
commands to make interacting with the Docker images easier. You've
already seen a few documented above, such as `build`, `rebuild`, and
`dev` (to run the containers). While interacting with the site, the
`superuser` command will allow you to easily create a new super user
(aliasing Django's own `createsuperuser`). While debugging, the
`bash`, `shell` (Python) and `dbshell` (MySQL) commands should be
useful.

### Running Commands Directly

The `Makefile` cannot account for all the possible interactions with
the docker containers or the scripts therein. While the various shells
should get you where you need to go, sometimes you will need to call
the docker containers directly. This may be done via the
`docker-compose` command.

Here are several quick examples with a full explanation of the command below.

To access the MySQL database directly:

    docker-compose exec mysql sh -c 'exec mysql -uroot -p'

To run Django commands within the `web` container:

    docker-compose run --rm web ./manage.py migrate
    docker-compose run --rm web ./manage.py collectstatic

_N.B._ --rm Remove container after run. Ignored in detached mode.

To see which containers are running, you may use the `docker-compose ps`
command, which will yield a list of containers like those below:

            Name                       Command               State             Ports
    -------------------------------------------------------------------------------------------
    impactapi_assets_1       /usr/bin/gulp                    Up       0.0.0.0:35729->35729/tcp
    impactapi_impactdata_1   sh                               Exit 0
    impactapi_mysql_1        docker-entrypoint.sh mysqld      Up       0.0.0.0:3307->3306/tcp
    impactapi_nginx_1        nginx -g daemon off;             Up       443/tcp, 80/tcp
    impactapi_redis_1        docker-entrypoint.sh redis ...   Up       6379/tcp
    impactapi_web_1          gunicorn --log-level info  ...   Up       0.0.0.0:8000->8000/tcp

Counterintuitively, when invoking commands on a container, you will
need to refer to the service name. The service name for the container is 
between the underscores in the name listed above; e.g.: `impactapi_nginx_1` 
is refered to as `nginx`.

You may alternatively list the services by invoking `docker-compose
config --services`.

With the service name in hand, you can then run commands on the running
container. For instance, to access the bash shell of the nginx service,
you would invoke:

    docker-compose exec nginx /bin/bash

You can do also do this via `make bash` from the impact-api directory.

### Running A Web Server Directly For Debugging Purposes

At times you may want to run a Django webserver locally
especially in the case where you have calls to pdb.set_trace()
and want to get to a debug prompt.

To run an interactive instance of Django:

    make runserver

This will stop the gunicorn supervisor process
and execute ```python3 manage.py runserver 0.0.0.0:8000```

You can now visit your locally running API instance at
http://localhost:8000/. It should give you some shell output at this
point.

Exiting runserver (via ctrl+c) kills the inline shell and restarts the
gunicorn daemon.

No additional action is needed after you exit the server.

You can also invoke a debugger inline by adding the following line in
your code:

   import pdb;pdb.set_trace()

Visiting a view that invokes the debug line will start a pdb prompt.
For a good resource on debugging in django see:
https://mike.tig.as/blog/2010/09/14/pdb/

### Internationalization and Translation via Django Rest Framework & Transifex

[The REST framework supports internationalization](http://www.django-rest-framework.org/topics/internationalization/)
and translation into many languages. This translation includes error messages
and the ability to limit or expand your language list as you see fit. The
translations are managed online using [Transifex](https://www.transifex.com/django-rest-framework-1/django-rest-framework/).

To add a new language to impact-api's Locale dir:

    django-admin makemessages -l -piglatin

Replace 'piglatin' with the [language code](
https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes)
for the language you would like the API to translate.

After adding a new language, you can add new strings for translation (and update previously added languages
with more strings).  

To add new strings:

    make messages

To compile these strings:

    make comp-messages


To see which language the API supports, you can run `make messages` to
see the current list of language codes. All of the [base translation
files]() can be found in the locale directory. `make comp-messages`
will also show you the path to each of the 'django.po' files in the
locale directory.

### Add New Strings for Translation

There are two ways to mark a string for translation. The first is to use a
[{% trans %} template tag](https://docs.djangoproject.com/en/1.10/topics/i18n/translation/#trans-template-tag})
or a [{% blocktrans %} template tag](https://docs.djangoproject.com/en/1.10/topics/i18n/translation/#blocktrans-template-tag).


    {% trans "string to translate" %}

To mark complex sentences that require literals and variables:

    {% blocktrans %}
        Here is a {{ var }}.
    {% endblocktrans %}

You can use [Lazy Translation](https://docs.djangoproject.com/en/1.10/topics/i18n/translation/#lazy-translation)
to translate strings when the value is accessed (rather than when
they're called).  To mark a string for translation in a python file,
make sure to import 'from django.utils.translation import
ugettext_lazy as _ ' and mark the beginning of a string with an
underscore.

Example:

    class Model(models.Model):
        full_name = models.CharField(_('full name'), max_length=200, blank=True)

### Granting Permissions

The `make grant-permissions` command can be used to assign django
permissions for a given user like so:

`make grant-permissions PERMISSION_CLASSES=view_startup,change_startup PERMISSION_USER=test@example.org`

To give a user access to the v1 api, issue the command with
'v1_clients' specified in PERMISSION_CLASSES:

`make grant-permissions PERMISSION_USER=test@example.org PERMISSION_CLASSES=v1_clients`

### Deployments

In order to deploy, you must first install and configure the AWS CLI
tool. Steps for setting this up can be found here:

http://docs.aws.amazon.com/cli/latest/userguide/installing.html

Install `aws` (version 1.14.14 or later): `pip install awscli`

Install `ecs` (version 1.4.3 or later): `pip install ecs-deploy`

You will also need to configure an AWS access key and secret key for
doing the deploy.  Steps for creating access keys can be found here:
http://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html#Using_CreateAccessKey

At the end of this process you should know both your access key and secret key.

You can confirm that you have minimally required version if the
following command returns any output:
```ecs deploy --help | grep "ignore-warnings"```

Once the CLI tools are installed and configured, you need to configure
your local AWS tools with the access key and secret key by running:

`aws configure`

This will prompt you for the access key and secret key.  The default
value is fine for the other options.

Next, login to AWS via the CLI:

`eval $(aws ecr get-login --region us-east-1);`

There are alternative ways of setting the secret keys so that the CLI
tools recognize your access keys.  You can find more information on
this by reading the documentation for boto:
http://boto3.readthedocs.org/en/latest/guide/configuration.html#configuration

#### Deploying to an Environment

To successfully deploy to ECS it is necessary for Travis to have a
successful build on the branch being deployed.  Travis is automatically
run each time a PR is created or updated.

Manage your secret keys and other sensitive information through
environment variables. The MassChallenge team manages our environment
variables in our Continuous Integration service,
[Travis](https://docs.travis-ci.com/user/environment-variables/).

Deploying to an environment is a matter of running ecs-deploy:

```
make deploy IMAGE_TAG=$IMAGE_TAG ENVIRONMENT=$ENVIRONMENT DOCKER_REGISTRY=$DOCKER_REGISTRY
```

An example of this to deploy current master to staging looks like this:
```
DOCKER_REGISTRY=`aws ecr describe-repositories --repository-name impact-api | cut -d"\"" -f4 | cut -d"/" -f1 | grep -i "amazonaws.com"`
make deploy IMAGE_TAG=master ENVIRONMENT=staging DOCKER_REGISTRY=$DOCKER_REGISTRY
```

The value for DOCKER_REGISTRY is expected to be a host name typically
ending with `.amazonaws.com`.  The hostname can be found at the top of
the [repositories
page](https://console.aws.amazon.com/ecs/home?region=us-east-1#/repositories/impact-api#images;tagStatus=ALL)
as part of the Repository URI.

A successful deploy will yield output that looks like the following:

```
Updating task definition
Changed image of container 'nginx' to: "<registry url>/nginx:AC-4034" (was: "<registry url>/nginx:AC-4034")
Changed image of container 'redis' to: "<registry url>/redis:AC-4034" (was: "<registry url>/redis:AC-4034")
Changed image of container 'web' to: "<registry url>/impact-api:AC-4034" (was: "<registry url>/impact-api:AC-4034")

Creating new task definition revision
Successfully created revision: 189
Successfully deregistered revision: 188

Updating service
Successfully changed task definition to: ecscompose-impact-api:189

Deploying task definition.................................................................................................................................................................................................................
Deployment successful
```

Note - if the IMAGE_TAG argument is not provided to the deploy
command, the name of the current branch is used as the IMAGE_TAG

The two main environments that you can push to are 'staging' and 'production'. 

Optional - A manual 'deploy' can also be triggered through the AWS ECS
interface. Reference the AWS documentation for details:
http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_run_task.html
