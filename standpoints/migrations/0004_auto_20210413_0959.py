# Generated by Django 3.1.7 on 2021-04-13 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('standpoints', '0003_auto_20210307_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='standpoint',
            name='link',
            field=models.CharField(max_length=150, unique=True, verbose_name='Länk'),
        ),
    ]
