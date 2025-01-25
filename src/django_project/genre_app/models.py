from uuid import uuid4
from django.db import models


# Create your models here.
class Genre(models.Model):
    app_label = "genre_app"
    id = models.UUIDField(primary_key=True, default=uuid4)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    categories = models.ManyToManyField("category_app.Category", related_name="genres")

    class Meta:
        db_table = "genre"
        verbose_name_plural = "Genres"
        verbose_name = "Genre"

    def __str__(self):
        return self.name
