from django.contrib import admin

from src.django_project.category_app.models import Category


# Register your models here.
class CategoryAdmin(admin.ModelAdmin): ...


admin.site.register(Category, CategoryAdmin)
