# Generated by Django 3.1.3 on 2021-01-08 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0011_auto_20201207_1550"),
    ]

    operations = [
        migrations.AlterField(
            model_name="game",
            name="deck",
            field=models.CharField(max_length=5000, null=True),
        ),
    ]
