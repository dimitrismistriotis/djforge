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

Command above populates the newly created `.env` with a new `SECRET_KEY`.
Not needed that much for development, necessary in production, see sub-section below.

### Production Environment

You need to have a custom secret key stored in the `SECRET_KEY` variable. You can
generate one with:

```shell
make secret_key
```

## User Management

After deliberation decided to use the [Substituting a custom User model](
https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#substituting-a-custom-user-model
) approach as discussed in the Django documentation.

Main concept is that we "override" the default `User` model with our own, which is
set in `settings.py` as `AUTH_USER_MODEL`. This is done in the `dj_users` app.
If you want to create another one, do so and adjust the `AUTH_USER_MODEL` value in
the settings file.

As documentation mentions:

> If you’re starting a new project, it’s highly recommended to set up
> a custom user model, even if the default User model is sufficient for you.
> This model behaves identically to the default user model, but you’ll be able
> to customize it in the future if the need arises

Plus:

> Don’t forget to point AUTH_USER_MODEL to it. Do this before creating
> any migrations or running manage.py migrate for the first time.

For this this is the first decision that needs to be made. If you want to "fork"
the `dj_users` app, you should do it first, before doing anything else that affects
the database.

### Pre-commit

We use [pre-commit](https://pre-commit.com/) to run some checks before committing.
There are different suggestions on how to install it, see: <https://pre-commit.com/#install>.
Seems that its authors would prefer it being installed externally from the Python
environment in which case `brew install pre-commit` is suggested given that
[Homebrew](https://brew.sh/) is available on your system.

Then run `make precommit_install` to attach it to the current repository.

Although we use it these checks for our code, it might not be necessary to use them
in a derived project as with most things listed here.

## Django Admin Access

Create a superuser with:

```shell
poetry run python manage.py createsuperuser
```

If you do not want to use Django's Admin interface, you can
remove the `django.contrib.admin` from the `INSTALLED_APPS` in `settings.py`.

If you want to heavily rely on Django Admin, see
[Awesome Django Admin](https://github.com/originalankur/awesome-django-admin?tab=readme-ov-file)
for themes and other extensions. We can discuss incorporating some of these in this
project.

## Install npm Packages

Run `make install_npm` to install npm packages for CSS generation.

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

This is a pattern to be followed on each "dj\_" prefixed app.
