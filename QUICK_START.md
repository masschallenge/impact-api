_MIT License_
_Copyright (c) 2017 MassChallenge, Inc._

## Quickstart for Impact-API

1. Install [Docker](https://docs.docker.com/docker-for-mac/)
(download the stable channel).

2. Start Docker from the Applications folder.

3. Run tests:

```
git clone https://github.com/masschallenge/impact-api.git
cd impact-api/
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
line should sya "BUILD COMPLETE"), visit http://localhost:8000 in a
browser to see the login screen.

5. In a separate shell, load an accelerate database.  If you have the
accelerate code base in a directory next to the impact-api source
code, then this will work:

```
make dbload GZ_FILE=../accelerate/test_data/initial_schema.sql.gz
```

6. Create a new superuser account:

```
make superuser
```

This will ask you for an email address, full name, short name and a
password.  For the purposes of this tutorial, we will assume the email
address is "admin@example.com".

6. Grant new account default access permissions

```
make grant-permissions PERMISSION_USER=admin@example.com PERMISSION_CLASSES=v0_clients,v1_clients
```

Rspond to the questions with "yes" or "y".

7. Go to http://localhost:8000 and login as admin@example.com.  At
this point you should be see a list of types of available accelerate
objects.  Clicking on one of those links should give a you short list
of some of the objects of the given type.  For example,
http://localhost:8000/api/impact/Application/

8. Next you need to create a client application.  Click the blue
"Create An Application" button near the top of the page followed by
"Register a new application".

9. Give your new client application a name, for "Client type" select
"Public" and for "Authorization grant type" select "Resource owner
password-based".  Click "Save".

10. Copy the value under "Client id".  Note that it is a 40 character
value that may not be completely visible.  However, double clicking it
and then copying should get the entire value.

11. Test functionally test the API, we recommend downloading Postman
(https://www.getpostman.com/) and loading in our testing collection
(https://www.getpostman.com/collections/b9dcecd3190fcd10888d).

12. Once this collection is loaded, go to the environment ("eye" icon
near the upper right corner).  Set the global variables "username",
"password", and "client_id" to the appropriate values from above.

13. Run the "oauth token" API token from the "initialization" folder
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

14. To test that you can access the data, open the "low-level" folder,
select "startup list" and click the blue "Send" button.  This
automatically selects a startup for subsequent call.  For example, if
you run the "startup" call, you will see which startup has been
selected.  Note the "short_pitch".

15. To test that you can change data, select the "startup patch" call.
Click the "Body" tab on the page.  The "short_pitch" should be
selected.  If you just click "Send" it will change the "short_pitch"
returned by the "startup" call.  You can click on the value of
"short_pitch" in the body of the "startup patch" call and then click
change to change it to any other value.

16. You can go through a similar process with system users, but
opening the "v1" folder and using the various "user" calls.  Note that
there is a "v1 user post" call.  This will create a new user using the
values given in the body of that call.  Creating a new user will
automatcally update Postman so it will be the subject of further calls
related the users.

17. The "v0" and "proxy" calls are historical calls that you probably
do not need to be concerned with.  The "proxy" calls require
additional setup to work since they access a live accelerate database.

