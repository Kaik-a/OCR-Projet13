# Generated by Django 3.1.3 on 2020-11-30 16:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("library", "0004_auto_20201128_0844"),
    ]

    operations = [
        migrations.AlterField(
            model_name="lendedgame",
            name="return_date",
            field=models.DateTimeField(default=None),
        ),
    ]