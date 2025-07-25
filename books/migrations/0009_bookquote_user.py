# Generated by Django 5.2.4 on 2025-07-24 21:46

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("books", "0008_rename_quote_bookquote_text"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="bookquote",
            name="user",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="quotes_user",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
