from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import Model, EmailField, BooleanField, ForeignKey, DO_NOTHING, DateTimeField, CharField, \
    OneToOneField, TextField


class AuthorizedAgent(models.Model):
    authorized = BooleanField(default=True)
    user = OneToOneField(settings.AUTH_USER_MODEL, default=None, blank=True, null=True, on_delete=DO_NOTHING)
    app_name = CharField(max_length=200, blank=True, null=True)
    app_key = TextField(blank=True, null=True)
    app_secret = TextField(blank=True, null=True)


class EmailAddress(Model):
    email = EmailField(blank=True, null=True)
    verified = BooleanField(default=False)
    primary = BooleanField(default=False)
    user = ForeignKey(get_user_model(), on_delete=DO_NOTHING)

    class Meta:
        db_table = "account_emailaddress"


class EmailConfirmation(Model):
    created = DateTimeField(auto_now_add=True, blank=True, null=True)
    sent = DateTimeField(blank=True, null=True)
    key = CharField(max_length=64, blank=True, null=True)
    email_address = ForeignKey(EmailAddress, null=True, on_delete=DO_NOTHING)

    class Meta:
        db_table = "account_emailconfirmation"
