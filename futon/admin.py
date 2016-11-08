from django.contrib import admin

from .models import Token, Site


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    pass


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    pass
