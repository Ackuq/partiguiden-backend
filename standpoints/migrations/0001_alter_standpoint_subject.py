# Generated by Django 3.2.4 on 2021-06-25 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("standpoints", "create_parties"),
    ]

    operations = [
        migrations.AlterField(
            model_name="standpoint",
            name="subject",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="standpoints",
                to="standpoints.subject",
                verbose_name="Sakområde",
            ),
        ),
    ]
