# Generated by Django 3.1.3 on 2020-11-28 08:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0003_auto_20201128_0823"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="lendedgame",
            unique_together={("owned_game", "return_date")},
        ),
    ]