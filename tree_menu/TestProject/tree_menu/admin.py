from django.contrib import admin
from tree_menu import models


@admin.register(models.Menu)
class MenuAdmin(admin.ModelAdmin):
    pass


@admin.register(models.MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    pass
