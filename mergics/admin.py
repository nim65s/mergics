from django.contrib.admin import site

from . import models

site.register(models.ICSInput)
site.register(models.ICSOutput)
