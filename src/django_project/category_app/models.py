from uuid import uuid4

from django.db import models


# Create your models here.
class Category(models.Model):
    app_label = "category_app"
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    description = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "category"
        verbose_name_plural = "Categories"
        verbose_name = "Category"

    def __str__(self):
        return self.name
