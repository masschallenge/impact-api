_MIT License_
_Copyright (c) 2017 MassChallenge, Inc._

# Documentation of the Impact API

## Accessing the API

The Impact API uses OAuth to manage authentication.  To get access you
must have an account on the MassChallenge Accelerate platform.

### Create an Accelerate Account

If you don't already have an Accelerate account:

1. Connect to MassChallenge Accelerate platform (During this initial
testing phase you should use the [Test 1 instance of the MassChallenge
Accelerate
platform](https://accelerate-test-1-elb-1625557903.us-east-1.elb.amazonaws.com)).

2. Register as an Entrepreneur by starting the [Register as a
Startup](https://accelerate-test-1-elb-1625557903.us-east-1.elb.amazonaws.com/accounts/register/entrepreneur/)
worflow.  Note that this is currently using a test site, so you may
get warnings about the connection being potentially insecure.

3. The email and password you use to create this account will be used
in the next sections.

### Register Your Use of the API

Afer logging in to https://api.masschallenge.org with your Accelerate
username and password, follow these steps:

1. Click "CREATE AN APPLICATION" at the top of the page.

2. Click "Register a new application".

3. In the resulting form, "Name" should describe your planned use of
the API.  E.g., "Public website: masschallenge.org".  The client type
should be "public" and the "Authorization grant type" should be
"Resource owner password-based".  The "Redirect uris" should be left
blank.

4. Click "Save".

5. Copy your "Client id" since this will be necessary to get access to
the API. If needed, you will be able to recover your Client Id(s)
through the [Impact-API](https://api.masschallenge.org) website.

6. Contact the administrators of the Impact API system to ensure that
your application is granted the permissions needed to access the API
calls you will be using.

## Trying Out the API

We recommend using the application
[Postman](https://www.getpostman.com/) for trying out the API.  We
have a Shared Postman Collection that can help you run various API
calls again the current server:

[![MC Collection](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/1c3cb99cd15a4c57f592)

You will need to provide values for the `username`, `password` and
`client_id` to the /oauth/token call.  This can be done in Postman by
clicking the "eye" icon in upper right corner, selecting "Edit", and
then adding the appropriate globals.

## Change from the Legacy API

- Because of the switch to OAuth, the `SecurityKey` parameter is no longer
  supported.
- The `SiteKey` parameter is no longer supported.  Site information is
  based on the instance of the Impact API that you are using combined
  with the permissions your account has.
- The `Format` parameter is no longer supported.  All calls only return
  JSON results.

## API Authorization

Before making any other API call, you will need to get an OAuth token
using the `/oauth/token/` API call.

### `/oauth/token`

Provide OAuth token for API access.

HTTP method: POST

#### Parameters:

* `username`: Your MassChallenge Accelerate account name.  Typically an
  email address.

* `password`: Your MassChallenge Accelerate password.

* `client_id`: The "Client id" for your registered application.

* `grant_type`: Should always be `password`.


#### Response: JSON object with the following names:

* `access_token`: Token needed for further API calls.

* `expires_in`: Time in seconds until this token expires.

* `token_type`: Type of the token.  Typically "Bearer".

* `scope`: Unused.

* `refresh_token`: Unused.


#### Example result:
```
{
  "access_token": "<access_token>",
  "expires_in": 36000,
  "token_type": "Bearer",
  "scope": "read write groups",
  "refresh_token": "<refresh_token>"
}
```


## v0 API

The v0 API is a reimplementation of the original API created to
support the original "Marketing" website.  This API is now being used
by the second generation public website.  The goal of the v0 API is to
allow that website to transition as smoothly as possible over to the
new impact-api server.  As a result this documentation will focus on
the changes from the original API.

For all v0 API calls the SecurityKey and SiteName should no longer be
used. Authorization is now handled by OAuth.  All calls should use an
access_token as returned by /oauth/token call.  This token should be
delivered in an `Authorization` HTTP header with a value of "Bearer
<access_token>".


### /api/v0/image/

Returns an image given an ImageToken from another API call.

HTTP method: GET

IMPORTANT: The ImageToken field should no longer be encrypted by
the client with the SecurityKey.  Just use the value returned by one
of the other API calls.

Note: You are encouraged to use image URLs rather than ImageTokens
when possible.  The next generation of the API is expected to
deprecate the use of ImageTokens and rely entirely on public APIs.

#### Parameters:

* `ImageToken`: As returned by startup_list, startup_detail, mentors
  and job_posting_detail calls.

* `ImageType`: JPEG or PNG.  Defaults to JPEG.

* `Size`: The size the returned image should be (example:
  200x200). Specified as widthxheight, width or xheight. Width and
  height are in pixels. Example values: 200x100, 200, x100.  Image is
  scaled to the given size and the aspect ratio preserved. If width
  and height are given the image is rescaled to maximum values of
  height and width given.

* `Crop`: Deprecated.

* `Upscale`: Deprecated.


#### Example result:
Image

### /api/v0/job_posting_detail/

Returns details on a specific job posting.

HTTP method: POST

Parameter:

* `JobKey`: Should be the id of a job posting as returned by the job_list
API call.

#### Response: JSON object with the following names:

* `startup_name`: Name of the startup with the job posting.

* `startup_profile_url`: URL to startup profile page.

* `startup_logo_image_token`: Image token for the startup logo.

* `title`: Job title for the posting.

* `type`: Job type. Currently supported values are:

  * `"A full-time contract position"`

  * `"A full-time permanent position"`

  * `"A part-time contract position"`

  * `"A part-time permanent position"`

  * `"An internship"`

* `application_email`: Email to send job applications to.

* `more_info_url`: URL to get more information on the posting.

* `description`: Description of the posting.

* `post_date`: Date the position was posted.

* `jobkey`: Unique id for this job posting.

#### Example result:
```
{
  "startup_name": "Startup 1234",
  "startup_profile_url": "http://masschallenge.org/startups/2016/profile/startup-1234",
  "startup_logo_image_token": "<imagetokenhash>=",
  "title": "Job Posting Title 283",
  "type": "A full-time permanent position",
  "application_email": "283-jobposting@example.com",
  "more_info_url": "",
  "description": "Great role at a great place!",
  "post_date": "2016-11-02",
  "jobkey": 283
}
```


### /api/v0/job_posting_list/

Returns a list of job postings.

HTTP method: POST

#### Parameters:

All parameters are optional. All parameters except OrderBy refine the full set of available
job postings.

* `JobType`: Supported values:

  * `FULL_TIME_CONTRACT`

  * `FULL_TIME_PERMANENT`

  * `INTERNSHIP`

  * `NONE`

  * `PART_TIME_CONTRACT`

  * `PART_TIME_PERMANENT`

* `Keywords`: Comma separated words and phrases to search for in the job posting.  The
  returned job postings must have at least one of the listed keywords.

* `OrderBy`: Supported values:

  * `jobtype`

  * `postdatedesc`

  * `startup`

* `ProgramKey`: Name or Id of a particular program associated with the startup with the
  job posting.

* `StartupKey`: Id or URL slug of a particular startup.  Startup ids are returned by
  the startup_list call.

#### Response: JSON object with the following names:

* `job_postings`: A list of the resulting job descriptions.  Job descriptions are the same
  as described in job_posting_detail call.

#### Example result:
```
{
  "job_postings": [
    {
      "startup_name": "Startup 1234",
      "startup_profile_url": "http://masschallenge.org/startups/2016/profile/startup-1234",
      "startup_logo_image_token": "<imagetokenhash>=",
      "title": "Job Posting Title 283",
      "type": "A full-time permanent position",
      "application_email": "283-jobposting@example.com",
      "more_info_url": "",
      "description": "Description 283 intentionally cleared",
      "post_date": "2016-11-02",
      "jobkey": 283
    }
  ]
}
```


### /api/v0/mentors/

Returns information on a set of mentors.

HTTP method: POST

#### Parameters:

* `NumItems: Required.  Number of mentors to return.

* `ProgramKey`: Name or Id of a particular program associated with the startup with the
  job posting.

#### Response: JSON object with the following names:

* `mentors`: A list of the resulting mentor descriptions.

Mentor descriptions are in turn JSON objects with the following name:

* `first_name`: First name of mentor.

* `last_name`: Last name of mentor.

* `company`: Mentor's company

* `title`: Mentor's title in that company

* `category`: Mentor's category. Possible values are:

  * `Executive`

  * `Investor`

  * `Lawyer`

  * `Other`

* `bio`: Mentor's biographical sketch.

* `public_website_consent`: Has this mentor agreed to have their information
  published publicly.

* `primary_industry`: The primary industry expertise string
  for this mentor.

* `additional_industries`: A list of additional industry
  expertise strings that apply to this mentor.

* `functional_expertise`: A list of functional expertise strings
  associated with this mentor.

* `photo_url`: URL to photo for this mentor.

* `image_token`: Image token which can be given to the images call.

#### Example result:
```
{
  "mentors": [
    {
      "first_name": "John",
      "last_name": "Doe",
      "company": "Doe, Inc.",
      "title": "Founder/CEO",
      "category": "Executive",
      "bio": "John Doe was born at a very young age and is awesome!",
      "public_website_consent": true,
      "primary_industry": "Healthcare / Life Sciences",
      "additional_industries": [
        "Healthcare IT"
      ],
      "functional_expertise": [
        "Product Development",
        "Strategy and Business"
      ],
      "photo_url": "https://accelerate.masschallenge.org/media/profile_pics/John_Doe.PNG",
      "image_token": "<imagetokenhash>="
    }
  ]
}
```

### /api/v0/startup_detail/

Returns details on a specific startup.

HTTP method: POST

#### Parameters:

* `ProgramKey`: Required.  Name or Id of a particular program.
  Only statuses related to the provided program are returned.

* `StartupKey`: Required.  Startup id or URL slug of a particular
  startup.  Startup ids are returned by the startup_list call.

#### Response: JSON object with the following names:

* `name`: Name of the startup.

* `is_visible`: Returns boolean indicating if this startup is "public"
  (vs. "stealth").

* `public_inquiry_email`: Contact email for startup.

* `short_pitch`: Startup pitch that is at most 140 characters.

* `full_elevator_pitch`: Longer (but still short) pitch.

* `video_elevator_pitch_url`: Optional URL to a short video about the
  startup.

* `primary_industry`: The primary industry industry relevant to this startup.

* `additional_industries`: A list of additional industries relevant to this
  startup.

* `statuses`: MassChallenge statuses for this startup.  Consists of a list of
  JSON objects that in turn have the following names:

  * `status_name`: Name of the MassChallenge status.

  * `status_badge_token`: Deprecated.

  * `status_badge_url`: Deprecated.

* `team_members`: List of Accelerate user accounts associated with
  this startup.  Consists of a list of JSON objects that in turn have
  the following names:

  * `first_name`: First name of the user.

  * `last_name`: Last name of the user.

  * `email`: Email/Accelerate account of the user.

  * `title`: Title of the user in this startup.

  * `photo_url`: URL to a photo of this user.

  * `photo_token`: ImageToken for the user.  Can be used with the image call
   to get the image.

* `website_url`: Optional website for the startup.

* `facebook_url`: Optional Facebook URL.

* `linked_in_url`: Optional LinkedIn URL.

* `twitter_handle`: Optional Twitter handle.

* `image_token`: ImageToken for this startup's logo.

* `logo_url`: URL to the startup's logo.

* `profile_background_color`: Deprecated.

* `profile_text_color`: Deprecated.

#### Example result:
```
{
  "additional_industries": [
    "Hardware & Robotics",
    "Internet of Things"
  ],
  "facebook_url": "http://facebook.com",
  "full_elevator_pitch": "Elevators are awesome!",
  "is_visible": true,
  "linked_in_url": "",
  "name": "Elevators-R-Us",
  "primary_industry": "Cybersecurity",
  "public_inquiry_email": "eru@example.com",
  "short_pitch": "Elevators!",
  "twitter_handle": "",
  "website_url": "http://example.com/ERU",
  "image_token": "<imagetokenhash>=",
  "logo_url": "http://accelerate.masschallenge.org/media/startup_pics/ERU.png",
  "profile_background_color": "#217181",
  "profile_text_color": "#FFFFFF",
  "statuses": [
    {
      "status_badge_token": "",
      "status_badge_url": "",
      "status_name": "2016 Diamond (BOS)"
    }
  ],
  "team_members": [
    {
      "first_name": "Elle",
      "last_name": "Vator",
      "email": "elle@example.com",
      "title": "",
      "photo_url": "",
      "photo_token": ""
    }
  ],
  "video_elevator_pitch_url": ""
}
```


### /api/v0/startup_list/

Returns a list of startups or groups of startups.

HTTP method: POST

#### Parameters:

* `ProgramKey`: Required.  Name or Id of a particular program.  If provided
  then only startups related to that program are returned.

* `StartupStatus`: Optional.  Startup status group name.  Supported values:

  * `entrants`

  * `finalists`

  * `top26`

  * `winners`

* `GroupBy`: Optional.  If provided, then startups are grouped into industry
  based lists.  The only supported value is Industry.

* `IncludeAllGroup`: Optional.  If "Y" and a "GroupBy" parameter is
  given, then an additional group called "All" is returned that lists all
  of the startups.  Supported values:

  * `Y` (the default)

  * `N`

#### Response: Structure of the response depends on whether the
GroupBy parameter is given.

If the GroupBy parameter is not given, then response is a JSON object with
the name:

* `startups`: A list of short startup descriptions.  Short startup
  descriptions are in turn JSON objects with the following names:

  * `id`: Unique id for this startup which can be used as a parameter
   to the startup_detail call.

  * `name`: Name of the startup.

  * `is_visible`: Returns boolean indicating if this startup is
  "public" (vs. "stealth").

  * `image_token`: ImageToken for this startup's logo.

  * `logo_url`: URL to the startup's logo.

  * `profile_url`: URL to the MassChallenge startup profile page.

  * `statuses`: MassChallenge statuses for this startup.  Consists of
    a list of JSON objects that in turn have the following names:

    * `status_name`: Name of the MassChallenge status.

    * `status_badge_token`: Deprecated.

    * `status_badge_url`: Deprecated.

#### Example result:
```
{
  "startups": [
    {
      "name": "Startup 1234",
      "id": 1234,
      "is_visible": true,
      "profile_url": "http://masschallenge.org/startups/2016/profile/startup-1234",
      "image_token": "<imagetokenhash>=",
      "logo_url": "http://accelerate.masschallenge.org/media/startup_pics/Startup1234.png",
      "statuses": [
        {
          "status_badge_token": "",
          "status_badge_url": "",
          "status_name": "2016 Diamond (BOS)"
        }
      ]
    },
    ...
  ]}
```

If the GroupBy parameter is given, then response is a JSON objects with
the following names:

* `groups`: A list of groups which in turn are JSON objects with the
  following names:

  * `group_title`: Supported values are:

    * `All`

    * `High Tech`

    * `Healthcare / Life Sciences`

    * `Energy / Clean Tech`

    * `Social Impact`

    * `General`

  * `startups`: List of JSON objects with the same names as described
  above.

  * `status`: Supported values are:

    * `Entrants`

    * `Finalists`

    * `top26`

    * `Winners`

  * `status_description`: Brief description of the status value.

#### Example result:
```
{
  "groups": [
    {
      "group_title": "High Tech",
      "startups": [
        {
          "is_visible": true,
          "name": "Startup 1234",
          "id": 1234,
          "profile_url": "http://masschallenge.org/startups/2016/profile/startup-1234",
          "image_token": "<imagetokenhash>=",
          "logo_url": "http://accelerate.masschallenge.org/media/startup_pics/startup-1234.png",
          "statuses": [
            {
              "status_badge_token": "",
              "status_badge_url": "",
              "status_name": "2016 Diamond (BOS)"
            }
          ]
        },
	...]},
    ...],
  "status": "Winners",
  "status_description": ""
}
```
