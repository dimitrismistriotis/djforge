# Setup

This is the setup guide on what to do after installing the project. It should be
as part of documentation, dropping it here in order not to create a dependency.

## Environment

Copy the `.env.dist` to `.env` and edit it accordingly if needed. Django Settings
provide defaults related to Docker Compose setup. Ideally because we wanted to shield
production environments from malfunctioning, `DEBUG` value is set to `False` by default.
For this the least necessary action is to have a oneline `.env` file with `DEBUG=True`.
You can do that with:

```shell
make create_dot_env_file
```

## Favicons

Used [FavIcons](https://www.favicon-generator.org/) to generate the favicons.
Chose a generic letter, "D" for "Django" and "DJ Forge" which would not be evasive in
a new project. Once you have decided on your logo you can create new icons using
a tool like the above and then replace the ones in the `dj_favicons/static/dj_favicons`
folder.

## Landing Page

Landing page is stored in the `dj_landing_page` app. It is a simple HTML page.
You can either edit it inline which might cause issues with feature updates or
leave it as it is, copy the directory to another one, then swap it on `INSTALLED_APPS`
within `settings.py` and edit `urls.py` to point to the new location.

This is a pattern to be followed on each "dj_" prefixed app.
