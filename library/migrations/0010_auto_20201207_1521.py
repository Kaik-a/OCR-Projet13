# Generated by Django 3.1.3 on 2020-12-07 15:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0009_auto_20201205_1843"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="lendedgame",
            unique_together={("owned_game", "returned", "return_date")},
        ),
    ]
