# Generated by Django 5.2.4 on 2025-07-23 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0004_bookquote"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="slug",
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
