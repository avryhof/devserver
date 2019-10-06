"""
@copyright Copyright KPH Healthcare Services, Inc., 2018

Urls for proact rx pharmacy services public pages.  Public pages are pages
that require no special permissions or login to view by anyone.
"""
from __future__ import unicode_literals

from django.urls import path

from .views import *

urlpatterns = [path("logout/", logout_view, name="logout"), path("login/", LoginView.as_view(), name="login")]
