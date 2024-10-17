# Generated by Django 5.1.2 on 2024-10-17 14:53

import django.db.models.deletion
import server.models
import server.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("server", "0003_category_icon_alter_server_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="channel",
            name="banner",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=server.models.server_banner_upload_path,
                validators=[server.validators.validate_image_file_extension],
            ),
        ),
        migrations.AddField(
            model_name="channel",
            name="icon",
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to=server.models.server_icon_upload_path,
                validators=[
                    server.validators.validate_icon_image_size,
                    server.validators.validate_image_file_extension,
                ],
            ),
        ),
        migrations.AlterField(
            model_name="server",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="server_category",
                to="server.category",
            ),
        ),
    ]
