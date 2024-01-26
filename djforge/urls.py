"""
URL configuration for djforge project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include
from django.urls import path

from dj_favicons.views import favicon
from dj_favicons.views import manifest_dot_json
from dj_landing_page.views import index_page

from .settings import INSTALLED_APPS

urlpatterns = [
    path("favicon.ico", favicon, name="favicon"),
    path("manifest.json", manifest_dot_json, name="manifest_dot_json"),
    path("", index_page, name="index"),
    path(
        "pages/",
        include("dj_content.urls"),
        name="dj_content",
    ),
    path(
        "register_interest",
        include("dj_register_interest.urls"),
        name="dj_register_interest",
    ),
]

if "django.contrib.admin" in INSTALLED_APPS:
    from django.contrib import admin

    urlpatterns += [
        path("admin/", admin.site.urls),
    ]
