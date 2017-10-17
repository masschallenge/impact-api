_MIT License_
_Copyright (c) 2017 MassChallenge, Inc._

## Quickstart for Impact-API

1. Install [Docker](https://docs.docker.com/engine/installation/#supported-platforms)
(download the stable channel).

2. Start Docker.

3. Get the source code.  If you already have impact-api checked out,
then in a Terminal window go to that directory and bring it up to date
with:
```
cd <impact-api-directory>
git checkout development
git pull
```

Note that the impact-api code is currently designed to work with an
instance of the MassChallenge Accelerate platform.  Specifically it
expects an instance of the Accelerate platform to manage a shared
database.  This quick start guide does not require a running version
of the Accelerate platform, but it does require an initial database
dump which is normally part of the accelerate code base.

If you don't have impact-api checked out, but you do have the
accelerate code base checked out, check out the impact-api code
next to the accelerate directory with:
```
cd <accelerate-directory>/..
git clone https://github.com/masschallenge/impact-api.git
cd impact-api
```

If you don't have the accelerate code base checked out, you will
need it to get an initial database.  If you need this, then contact
engineering@masschallenge.org.

4. Run tests.  From the impact-api source directoy run:
```
make build
make test
```

This will take a while, but all tests should pass.  Specifically the
end of the output should look something like:

```
Ran 102 tests in 14.845s

OK
Destroying test database for alias 'default'...
```

4. Start server

```
make dev
```

Once the process completes (it will take a little while and the last
line should say "BUILD COMPLETE"), visit http://localhost:8000 in a
browser to see the login screen.

5. In a separate shell, load an accelerate database.  Assuming
you have an up-to-date accelerate source code directory next to
the impact-api directory, the following should work:

```
make dbload GZ_FILE=../accelerate/db_cache/initial_schema.sql.gz
```

6. Create a new superuser account:

```
make superuser
```

This will ask you for an email address, full name, short name and a
password.  For the purposes of this tutorial, we will assume the email
address is "admin@example.com".

7. Grant new account default access permissions

```
make grant-permissions PERMISSION_USER=admin@example.com PERMISSION_CLASSES=v0_clients,v1_clients
```

Respond to any confirmation prompts with "yes" or "y".

8. Go to http://localhost:8000 and log in as admin@example.com.  At
this point you should be see a list of types of available accelerate
objects.  Clicking on one of those links should give a you short list
of some of the objects of the given type.  For example,
http://localhost:8000/api/impact/Application/

9. Next you need to create a client application.  Click the blue
"Create An Application" button near the top of the page followed by
"Register a new application".

10. Give your new client application a name, for "Client type" select
"Public" and for "Authorization grant type" select "Resource owner
password-based".  "Redirect URIs" should not be given.  Click "Save".

11. Copy the value under "Client id".  Note that it is a 40 character
value that may not be completely visible.  However, double clicking it
and then copying should get the entire value.

12. To functionally test the API, we recommend downloading Postman
(https://www.getpostman.com/) and importing our testing collection.
To import a collection into Postman go to File -> Import and select
the "Import From Link" tab, insert the URL
https://www.getpostman.com/collections/b9dcecd3190fcd10888d and click
"Import".

13. Once this collection is loaded, go to the environment ("eye" icon
near the upper right corner).  Add the global variables "username",
"password", and "client_id" to the appropriate values from above.

14. Run the "oauth token" API token from the "initialization" folder
by selecting it and clicking "Send".  This should give a response that
looks like:

```
{
    "access_token": "XXX",
    "expires_in": 36000,
    "token_type": "Bearer",
    "scope": "read write groups",
    "refresh_token": "XXX"
}
```

Postman will automatically parse this an enable the other calls to use
this access token.

15. To test that you can access the data, open the "low-level" folder,
select "startup list" and click the blue "Send" button.  This
automatically selects a startup for subsequent call.  For example, if
you run the "startup" call, you will see which startup has been
selected.  Note the "short_pitch".

16. To test that you can change data, select the "startup patch" call.
Click the "Body" tab on the page.  The "short_pitch" should be
selected.  If you just click "Send" it will change the "short_pitch"
returned by the "startup" call.  You can click on the value of
"short_pitch" in the body of the "startup patch" call and then click
change to change it to any other value.

It should be noted that due to client, browser, or firewall restrictions, it may be necessary to send PATCH calls as POSTS and override them.  The middleware which overrides these types of POSTs is included in the code base.  To PATCH via POST (override the POST), you will need to include the following header/value pair: 'HTTP_X_HTTP_METHOD_OVERRIDE':'PATCH'.

17. You can go through a similar process with system users, by
opening the "v1" folder and using the various "user" calls.  Note that
there is a "v1 user post" call.  This will create a new user using the
values given in the body of that call.  Creating a new user will
automatically update Postman so it will be the subject of further calls
related the users.

18. The "v0" and "proxy" calls are historical calls that you probably
do not need to be concerned with.  The "proxy" calls require
additional setup to work since they access a live accelerate database.
