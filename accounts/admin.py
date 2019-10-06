from django.contrib import admin

from .models import EmailAddress, EmailConfirmation, AuthorizedAgent


@admin.register(AuthorizedAgent)
class AuthorizedAgentAdmin(admin.ModelAdmin):
    list_display = ("app_name", "user", "authorized")
    list_filter = ("authorized", "user")


@admin.register(EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ("email", "verified", "primary", "user")
    list_filter = ("verified", "primary", "user")
    search_fields = ("email", "user__username")


@admin.register(EmailConfirmation)
class EmailConfirmationAdmin(admin.ModelAdmin):
    list_display = ("email_address", "created", "sent")
    list_filter = ("created", "sent", "email_address")
    search_fields = ("email_address__email", "email_address__user__username")
