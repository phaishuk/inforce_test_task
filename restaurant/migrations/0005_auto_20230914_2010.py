# Generated by Django 4.2.5 on 2023-09-14 20:10

from django.db import migrations
from django.core.management import call_command


def load_func(apps, schema_editor):
    call_command("loaddata", "data.json")


def to_unload_func(apps, schema_editor):
    pass


class Migration(migrations.Migration):
    dependencies = [
        (
            "restaurant",
            "0004_alter_menu_lunch_date",
        ),
    ]

    operations = [
        migrations.RunPython(load_func, to_unload_func),
    ]
