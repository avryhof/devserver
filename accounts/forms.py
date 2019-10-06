from django.forms import Form, CharField, PasswordInput, BooleanField, CheckboxInput


class LoginForm(Form):
    username = CharField()
    password = CharField(widget=PasswordInput())
    remember_username = BooleanField(initial=True, widget=CheckboxInput())
