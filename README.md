_MIT License_
_Copyright (c) 2017 MassChallenge, Inc._

# Impact API Server


 [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://travis-ci.org/masschallenge/impact-api.svg?branch=development)](https://travis-ci.org/masschallenge/impact-api)
<a href="https://codeclimate.com/github/masschallenge/impact-api/maintainability">
  <img src="https://api.codeclimate.com/v1/badges/919b52c7bf78bfc67bb6/maintainability" />
</a>
 

## Quickstart

* **For Installation Instructions that include Accelerate, see [here](
https://github.com/masschallenge/standards/blob/AC-5050/setup_development_environment.md)**.


1. Make sure you have the following installed:
   - [Docker](https://docs.docker.com/docker-for-mac/) (download the stable channel).
   - git
   - GNU Wget
   - GNU Make
   - (some deprecated commands require the installation and configuration of
   python2.7 with ecs, ecs-cli and aws-cli)
2. If just installed, start Docker from the Applications folder.
3. Build the project.

    ```
    
    git clone https://github.com/masschallenge/impact-api.git
    git clone https://github.com/masschallenge/django-accelerator.git
    cd impact-api/
    make run-server
    ```

4. Once the process completes (it will take a few minutes), visit
http://localhost:8000 in a browser.

5. Shutdown and cleanup.

    ```
    shutdown-vms
    ```
    
* To see all available commands, run `make help`.

## Commands

This section describes the more common commands you may
need when working on this platform. For a full list of the
commands, refer to `make help`.

### Rebuilding the container

This should be done whenever the project's dependencies
change, e.g. Python [requirements](
https://github.com/masschallenge/impact-api/tree/development/web/impact/requirements)
, or one of the [Dockerfiles](
https://github.com/masschallenge/impact-api/blob/development/web/Dockerfile).

This can be done with:

    `make build;make run-server;`
    
* Note that `make build` deletes the DB, so any 
changes you've made before to the database should be re-applied.
* It is possible to specify a dump file to load, by running
`make build;make run-server gz_file=<path_to_file.sql.gz>`.
  * Combining this option with `make dump-db db_name=<name>` will
  allow you to keep the state after a re-build

### Managing The Local Database

We maintain a copy of production database with cleaned and 
anonymized data, that is made available for local development. 

The db-dump file is named `initial_schema.sql.gz`, and is 
the implicit default of all database-related commands.

loading a copy of the database dump into to mysql database, 
can be done by running `make load-db`. Unapplied migrations will
be executed as well. Running `make load-remote-db` will 
first clear the local cached copy of this file, if exists.

For more advanced use cases, see [Database Management](https://github.com/masschallenge/standards/blob/master/database_management.md) or `make help`.

### Creating a release:

See [Standards](
https://github.com/masschallenge/standards/blob/master/create_new_release.md).

### Accessing The Shell
* In order to access the default shell of the Docker container
on which the Django project is running (service "web"), run `make bash-shell`.
* In order to access the Django shell, run `make django-shell`.
* In order to access the mysql shell, run `make db-shell`.


### Running A Web Server In Supervisor/Debug Mode


#### Debug Mode (default)

Usually, you'll want to run a Django webserver locally,
especially in the case where you have calls to pdb.set_trace()
and want to get to a debug prompt.

To run an interactive instance of Django, run 
`make run-server`, or one of its aliases:

`make run-server-1`
or
`make run-server debug=1`

* Note that exiting run-server (via ctrl+c) will **not** kill
the server, but instead it will return to detached mode, and
run in the background.
To stop the server, run `make stop-server` as well.

* In this mode you can also invoke a debugger inline
by adding the following line in your code: 
`import pdb;pdb.set_trace()`. Visiting a view 
that invokes the debug line will start a pdb prompt.
For a good resource on debugging in django see:
https://mike.tig.as/blog/2010/09/14/pdb/


#### Supervisor Mode
At times, you may want to see the gunicorn + supervisor
server as is being run in production. This mode also shows
a more detailed output of the docker-compose up command 
that is executed in the background.

This can be done by running
`make run-server-0`
or
`make run-server debug=0`

Visiting your locally running API instance at
http://localhost:8000/, will now show the output
for the respective running mode.

No additional action is needed after you exit the server.

### Granting Permissions (Depracated):

The `make grant-permissions` command can be used to assign django
permissions for a given user like so:

`make grant-permissions PERMISSION_CLASSES=view_startup,change_startup PERMISSION_USER=test@example.org`

To give a user access to the v1 api, issue the command with
'v1_clients' specified in PERMISSION_CLASSES:

`make grant-permissions PERMISSION_USER=test@example.org PERMISSION_CLASSES=v1_clients`

### Release and Deploy

Impact-api is configured such that every successful Travis build
is made available as a deployable image in AWS ECS. Accelerate's
Deploy command in OpsWorks is configured to also trigger a deploy
for impact-api, automatically. 

**For this automatic deploy to work, it is required that the 
specified revision (tag/branch) exists both in Accelerate and 
in impact-api**.

For a detailed explanation or our release steps, see our [standards](
https://github.com/masschallenge/standards/blob/master/create_new_release.md)

* A manual 'deploy' can also be triggered through the AWS ECS
interface, independent of an Accelerate deploy. Reference 
the AWS documentation for details, [here](
http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs_run_task.html).


### Running Docker Commands Directly

The `Makefile` cannot account for all the possible interactions with
the docker containers or the scripts therein. While the various shells
should get you where you need to go, sometimes you will need to call
the docker containers directly. This may be done via the
`docker-compose` command.

Here are several quick examples with a full explanation of the command
below.

To access the shell in the MySQL container directly:

    docker-compose exec mysql /bin/bash

To run Django commands within the `web` container:

    docker-compose run --rm web ./manage.py showmigrations
    docker-compose run --rm web ./manage.py collectstatic

_N.B._ --rm flag Removes the container after execution run.

To see which containers are running, you may use the `docker-compose ps`
command, which will yield a list of containers like those below:
```
MC-DEV-YMANOR:impact-api yotammanor$ docker-compose ps
             Name                           Command               State                                 Ports                              
-------------------------------------------------------------------------------------------------------------------------------------------
impactapi_assets_1               /usr/bin/gulp                    Exit 1                                                                   
impactapi_mysql_1                docker-entrypoint.sh mysqld      Up       0.0.0.0:3307->3306/tcp                                          
impactapi_redis_1                docker-entrypoint.sh redis ...   Up       0.0.0.0:6379->6379/tcp                                          
impactapi_start_dependencies_1   /bin/bash -c  until $(curl ...   Exit 0                                                                   
impactapi_web_1                  /bin/bash /usr/bin/start.sh      Up       0.0.0.0:443->443/tcp, 0.0.0.0:80->80/tcp, 0.0.0.0:8000->8000/tcp
```

Counterintuitively, when invoking commands on a container, you will
need to refer to the service name. The service name for the container is 
between the underscores in the name listed above; e.g.: `impactapi_web_1` 
is refered to as `web`.

You may alternatively list the services by invoking `docker-compose
config --services`.

With the service name in hand, you can then run commands on the running
container. For instance, to access the bash shell of the nginx service,
you would invoke:

    docker-compose exec web /bin/bash

This is equivalent to running `make bash-shell`.

# NO MERGE
# no merge 1
# no merge 2

