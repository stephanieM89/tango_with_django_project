"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from rango import views


urlpatterns = [
    url(r'^$', views.index, name='index'),  # This maps the basic url to the index view in the rango app
    url(r'about/$', views.about, name='about'),
    url(r'^rango/', include('rango.urls')),  # Maps any URLs starting with rango/ to be handled by the rango app
    url(r'^admin/', admin.site.urls), # For every URL starting with admin/ Django will find a corresponding view
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


