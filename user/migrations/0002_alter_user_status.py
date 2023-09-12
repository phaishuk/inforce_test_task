# Generated by Django 4.2.5 on 2023-09-11 19:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="status",
            field=models.CharField(
                choices=[
                    ("rest_rep", "Restaurant representative"),
                    ("employee", "Employee"),
                ],
                max_length=20,
            ),
        ),
    ]