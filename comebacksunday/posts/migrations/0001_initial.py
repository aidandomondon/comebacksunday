# Generated by Django 5.2.1 on 2025-05-31 03:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="ExtendedUser",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        related_name="extendeduser",
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "bio",
                    models.TextField(
                        max_length=100, verbose_name="Short self-description of user."
                    ),
                ),
                (
                    "private",
                    models.BooleanField(
                        default=False,
                        verbose_name="Only followers can see this user's posts?",
                    ),
                ),
                (
                    "following",
                    models.ManyToManyField(
                        related_name="followers",
                        to="posts.extendeduser",
                        verbose_name="Users this user is following.",
                    ),
                ),
                (
                    "requested_followers",
                    models.ManyToManyField(
                        related_name="+",
                        to="posts.extendeduser",
                        verbose_name="Users with pending requests to follow this user",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("content", models.TextField(max_length=280)),
                (
                    "datetime",
                    models.DateTimeField(
                        auto_now_add=True,
                        verbose_name="Date and time this post was made.",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="posts.extendeduser",
                        verbose_name="Author of this post",
                    ),
                ),
            ],
        ),
    ]
