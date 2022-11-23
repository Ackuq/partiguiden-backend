from django.db import migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps


PARTIES = [
    {"id": "S", "name": "Socialdemokraterna"},
    {"id": "M", "name": "Moderaterna"},
    {"id": "SD", "name": "Sverigedemokraterna"},
    {"id": "V", "name": "Vänsterpartiet"},
    {"id": "C", "name": "Centerpartiet"},
    {"id": "KD", "name": "Kristdemokraterna"},
    {"id": "MP", "name": "Miljöpartiet"},
    {"id": "L", "name": "Liberalerna"},
]


def create_parties(apps: StateApps, schema_editor: BaseDatabaseSchemaEditor) -> None:
    Party = apps.get_model("standpoints", "Party")
    db_alias = schema_editor.connection.alias

    for party in PARTIES:
        if not Party.objects.using(db_alias).filter(id=party["id"]).exists():
            Party.objects.using(db_alias).create(id=party["id"], name=party["name"])


class Migration(migrations.Migration):

    dependencies = [("standpoints", "0004_auto_20210413_0959")]

    operations = [migrations.RunPython(create_parties)]
