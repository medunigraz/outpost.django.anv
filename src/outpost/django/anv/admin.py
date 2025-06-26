from django.contrib import admin

from . import models


@admin.register(models.System)
class SystemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Station)
class StationAdmin(admin.ModelAdmin):
    pass
