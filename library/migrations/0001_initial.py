# Generated by Django 3.1.3 on 2020-11-23 15:05

import datetime
import uuid

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Game",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("deck", models.CharField(max_length=5000)),
                ("image", models.CharField(max_length=1000)),
                ("giantbomb_url", models.CharField(max_length=500)),
                ("release_date", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Platform",
            fields=[
                (
                    "name",
                    models.CharField(
                        max_length=100, primary_key=True, serialize=False, unique=True
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ownedGame",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "acquisition_date",
                    models.DateTimeField(default=datetime.datetime.now),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="library.game"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "game")},
            },
        ),
        migrations.CreateModel(
            name="lendedGame",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                ("not_registered_borrower", models.CharField(max_length=100)),
                ("lended_date", models.DateTimeField(default=datetime.datetime.now)),
                ("return_date", models.DateTimeField(null=True)),
                (
                    "borrower",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="library.ownedgame",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="game",
            name="platform",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="library.platform"
            ),
        ),
        migrations.CreateModel(
            name="WantedGame",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4, primary_key=True, serialize=False
                    ),
                ),
                (
                    "game",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="library.game"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "game")},
            },
        ),
        migrations.AlterUniqueTogether(
            name="game",
            unique_together={("name", "giantbomb_url")},
        ),
    ]
