from django.db import migrations


def create_default_subject(apps, schema_editor):
    db_alias = schema_editor.connection.alias
    Subject = apps.get_model("standpoints", "Subject")
    Subject.objects.using(db_alias).create(name="uncategorized")


class Migration(migrations.Migration):
    dependencies = [
        ("standpoints", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_subject),
    ]
