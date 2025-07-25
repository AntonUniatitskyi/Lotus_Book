# Generated by Django 5.2.4 on 2025-07-23 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="cover",
            field=models.ImageField(blank=True, null=True, upload_to="covers/"),
        ),
        migrations.AddField(
            model_name="book",
            name="text_author",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="book",
            name="text_book",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="profile",
            name="avatar",
            field=models.CharField(
                blank=True,
                choices=[
                    ("avatars/default-avatar.jpg", "Дефолт"),
                    ("avatars/boy-brunet.png", "Брюнет"),
                    ("avatars/girl-blond-long.png", "Блондинка"),
                    ("avatars/girl-brunet-long.png", "Брюнетка"),
                    ("avatars/girl-brunet-short.png", "Коротка брюнетка"),
                ],
                default="avatars/default-avatar.jpg",
                max_length=255,
            ),
        ),
    ]
