from django.contrib import admin
from .models import Professors, Modules, Ratings

admin.site.register(Professors)
admin.site.register(Modules)
admin.site.register(Ratings)

# Register your models here.
