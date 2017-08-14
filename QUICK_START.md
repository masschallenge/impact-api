_MIT License_
_Copyright (c) 2017 MassChallenge, Inc._

# Impact API Server

## Quickstart

1. Install [Docker](https://docs.docker.com/docker-for-mac/)
   (download the stable channel).

2. Start Docker from the Applications folder.

3. Run tests:

    git clone https://github.com/masschallenge/impact-api.git
    cd impact-api/
    make test

All tests should pass.

4. Start server

    make dev

Once the process completes (it will take a little while and the last
line should sya "BUILD COMPLETE"), visit http://localhost:8000 in a
browser to see the login screen.

5. In a separate shell, load an accelerate database.  If you have the
accelerate code base in a directory next to the impact-api source
code, then this will work:

    make dbload GZ_FILE=../accelerate/test_data/initial_schema.sql.gz

6. Create a new superuser account:

    make superuser

This will ask you for an email address, full name, short name and
a password.  For the purposes of this tutorial, we will assume the
email address is "admin@example.com".

6. Grant new account default access permissions

    make grant-permissions PERMISSION_USER=admin@example.com PERMISSION_CLASSES=v0_clients,v1_clients

Rspond to the questions with "yes" or "y".

7. Go to http://localhost:8000 and login as admin@example.com.

8. Click "Create An Application" followed by "Register a new application".

9. Give your new client application a name, for "Client type" select "Public"
and for "Authorization grant type" select "Resource owner password-based".
Click "Save".

10. Copy the value under "Client id".  Note that it is a 40 character
value that may not be completely visible.  However, double clicking it
and then copying should get the entire value.

11. Test functionally test the API, we recommend downloading
Postman (https://www.getpostman.com/) and loading in our testing collection
(https://www.getpostman.com/collections/b9dcecd3190fcd10888d).

12. Once this collection is loaded, go to the environment ("eye" icon
near the upper right corner).  Set the global variables "username",
"password", and "client_id" to the appropriate values from above.

13. Run the "oauth token" call by selecting it and clicking "Send".

14. Run the "startup list" under the "low-level" folder call by
selecting it and clicking "Send".
