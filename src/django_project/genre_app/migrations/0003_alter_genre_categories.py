# Generated by Django 5.0.1 on 2025-01-13 02:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("category_app", "0002_alter_category_options"),
        ("genre_app", "0002_alter_genre_categories"),
    ]

    operations = [
        migrations.AlterField(
            model_name="genre",
            name="categories",
            field=models.ManyToManyField(
                related_name="genres", to="category_app.category"
            ),
        ),
    ]
