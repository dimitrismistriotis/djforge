# Setup

This is the setup guide on what to do after installing the project. It should be
as part of documentation, dropping it here in order not to create a dependency.

## Environments

## Development Environment

You can either fork the repository or create another one using this as a template
as discussed here: [Creating a repository from a template](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template)

Copy the `.env.dist` to `.env` and edit it accordingly if needed. Django Settings
provide defaults related to Docker Compose setup. Ideally because we wanted to shield
production environments from malfunctioning, `DEBUG` value is set to `False` by default.
For this the least necessary action is to have an one line `.env` file with `DEBUG=True`.
You can do that with:

```shell
make create_dot_env_file
```

Command above populates the newly created `.env` with a new `SECRET_KEY`.
Not needed that much for development, necessary in production, see sub-section below.

## Package Management

We settled for [uv](https://docs.astral.sh/uv/) - [github](https://github.com/astral-sh/uv). Check its "[Installation](https://docs.astral.sh/uv/getting-started/installation/)" section on how to set up.

### Node.js for Tailwind CSS and React.Email

[Node.js](https://nodejs.org/en/) needs to be available alongside `npm` and `npx`.
Because of different types of setups in different operating systems or distributions,
how to do install is left out as "out of scope" of this document. Easiest way is to
is using [brew](https://brew.sh/).

Node is needed for two reasons: Tailwind CSS compilation, and email template generation.
You can develop without it, but extra CSS classes of Tailwind or own have to be
added manually. Similar situation for email templates.

Then run:

```shell
npm install tailwindcss @tailwindcss/cli flowbite
```

Outputs of the above should be placed in version control and presence of these tools
in production is not required, not we believe should be for a Django project.

### Helpers

#### pgAdmin

<https://www.pgadmin.org/>

> pgAdmin is the most popular and feature rich Open Source administration and
> development platform for PostgreSQL, the most advanced Open Source database
> in the world.

There is an instance of pgAdmin running as a container alongside Postgres.
It is accessible in port 5050.

-   Use your browser to navigate to: <http://localhost:5050>.
-   Default login email from `docker-compose.yml` is **pgadmin@djforge.net** and default password is **pgadmin_password**.
-   Development server's details are prepopulated, pgAdmin does not allow to prepopulate the password of the database which is: **dj_forge_password**

### React.email

Homepage: [React.email](https://react.email/)

Used to create nice emails in HTML and text format. What is provided is the self contained application produced from installation instructions here: <https://react.email/docs/getting-started/automatic-setup> plus wrappers in the makefile for ease of use. Additionally, the generated templates for this application's emails are also provided.

You can either edit the template since it is in uncompressed HTML plus text and ignore this helper, or use it to create completely custom emails. After some experimentation we discovered that it is best to have final emails not generated hene place them into their own folder.

Install packages and update react.email periodically with:

```shell
make update_react_email
```

Run with:

```shell
make react_email
```

## Production Environment

You need to have a custom secret key stored in the `SECRET_KEY` variable. You can
generate one with:

```shell
make secret_key
```

### Environment Variables

Although defaults are for production, it is suggested to also add them through the desired hosting solution:

-   **DEBUG**: to `false`, unless you want to debug something in production
-   **ENVIRONMENT**: to `production`

#### Health Check

For many providers or provisioners, a health check endpoint is necessary.
We have one at `/pages/health` which returns a 200 status code "OK" message as a
response.

Example run with httpie in local development environment:

```shell
http http://localhost:8000/pages/health
HTTP/1.1 200 OK
Content-Length: 2
Content-Type: text/html; charset=utf-8
Cross-Origin-Opener-Policy: same-origin
Date: Fri, 29 Mar 2024 16:03:49 GMT
Referrer-Policy: same-origin
Server: WSGIServer/0.2 CPython/3.12.2
Vary: Cookie
X-Content-Type-Options: nosniff
X-Frame-Options: DENY

OK
```

### Deployments

#### Render.com

Did our first deployment on Render.com.

Followed instructions on
[Deploying Django on Render](https://docs.render.com/deploy-django)
tweaking them for DJ-Django's configuration. For example did not install
DJ-Database-URL, used poetry, `make build` instead of a build script,
and others.

In order to deploy a project there, having created an account, follow
the steps in "Use render.yaml for deploys" (same URL as above), in detail:

1. _Create a file named render.yaml..._ this has already beed done in
   `render.yaml` in the root of this project. Check it and edit it if needed,
   for example if the name of the application has changed
2. In the Render Dashboard, go to the Blueprints page and click New Blueprint Instance.
3. Select the repository that contains your blueprint and click Connect.
4. Give your blueprint project a name and click Apply.

Render.com should take care of the rest:

> That’s it! Your project will be live at
> its .onrender.com URL as soon as the build finishes.

If you have a custom domain: Go to "Settings" -> "Custom Domains" and add it there.
It will give you entries to add to your DNS provider.

Note: these are instructions for the "free" package, without async processing
or other related functionality. We will be updating this section as we
implement/configure them.

## User Management

After deliberation decided to use the [Substituting a custom User model](https://docs.djangoproject.com/en/5.0/topics/auth/customizing/#substituting-a-custom-user-model) approach as discussed in the Django documentation.

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

## Task Queue - Asynchronous Tasks

As the project currently is [Celery](https://docs.celeryq.dev/en/stable/index.html)
is installed and configured to be used with a Redis back end which is one of the
containers in `docker-compose.yml`. Currently it is not used integrally to the project,
with this most probably to change soon. Some tasks to get an idea on how to write
code with it are in the `dj_tasks` application inside `tasks.py`.

From Celery's documentation:

> Task queues are used as a mechanism to distribute work across threads or machines.

> A task queue's input is a unit of work, called a task, dedicated worker processes
> then constantly monitor the queue for new work to perform.

> Celery communicates via messages, usually using a broker to mediate between
> clients and workers. To initiate a task a client puts a message on the queue,
> the broker then delivers the message to a worker.

> A Celery system can consist of multiple workers and brokers, giving way to
> high availability and horizontal scaling.

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

Change the name in `dj_favicons/templates/dj_favicons/manifest.json` to something
that matches your project.

## Landing Page

Landing page is stored in the `dj_landing_page` app. It is a simple HTML page.
You can either edit it inline which might cause issues with feature updates or
leave it as it is, copy the directory to another one, then swap it on `INSTALLED_APPS`
within `settings.py` and edit `urls.py` to point to the new location.

This is a pattern to be followed on each "dj\_" prefixed app.

## Email Dispatch

### Development

Currently there is email capture with Mailcrab which traps SMTP traffic in 1025 port
and exposes a web service in 1080.

### Resend.com

Optional integration of [Resend.com](https://resend.com/). For how to setup and
validate the domain check their documentation and guides. For this application, make
`RESEND_API_KEY` available to the application (same name as one in Resend's
documentation).

## Proof of Concept Area

### Maps Page

In order to display the Map image and link, a Google Maps API key is needed to be
set as the `GOOGLE_MAPS_API_KEY` variable, stemming from environment.
For instructions see
<https://developers.google.com/maps/documentation/javascript/get-api-key>
or search the web 🙃: <https://search.brave.com/search?q=create+google+maps+api+key>

### Permissions Check Page

A page checking permissions displayed conditionally, to be used as a reference for
permission checks within the app.

You can add a user to a group programmatically from shell_plus with:

```python
>>> Group.objects.get(
   name="Platform Administrators").user_set.add(User.objects.get(
   email="john.doe@example.com"))
```

## Updating Repositories Generated from Template

One solution would be to use [Cruft](https://github.com/cruft/cruft) which has
automated the process. Unfortunately this requires the repository to be formed with
CookieCutter, something that it is not for the time being at least.

Had good results with <https://github.com/AndreasAugustin/actions-template-sync> which
is currently the most suggested option, after having it configured.

Most suggested option is to generate from a template and then
"fork" each Django application: copy to new directory and change in `settings.py`.
Then at regular intervals copy over from original repository and then port each
change you want.
