# Generated by Django 5.0.1 on 2025-01-11 23:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("category_app", "0002_alter_category_options"),
        ("genre_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genre",
            name="categories",
            field=models.ManyToManyField(
                blank=True, default=None, to="category_app.category"
            ),
        ),
    ]
