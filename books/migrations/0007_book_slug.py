# Generated by Django 5.2.4 on 2025-07-23 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0006_remove_book_slug"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
