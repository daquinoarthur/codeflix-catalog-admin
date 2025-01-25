from django.contrib import admin
from .models import Genre


# Register your models here.
class GenreAdmin(admin.ModelAdmin): ...


admin.site.register(Genre, GenreAdmin)
