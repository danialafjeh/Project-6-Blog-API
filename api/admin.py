from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Category)
admin.site.register(models.Tag)
admin.site.register(models.BlogPost)
admin.site.register(models.Like)
admin.site.register(models.Comment)
