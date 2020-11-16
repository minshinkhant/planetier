from django.contrib import admin
from . import models


class PlanetyMemberInline(admin.TabularInline):
    model = models.PlanetyMember


admin.site.register(models.Planety)
