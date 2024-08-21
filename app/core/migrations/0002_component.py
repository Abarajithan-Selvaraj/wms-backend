# Generated by Django 5.1 on 2024-08-20 14:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),       # noqa: E501
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(blank=True)),
                ('version', models.TextField()),
                ('type', models.TextField(max_length=255)),
                ('level', models.IntegerField()),
                ('index', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),      # noqa: E501
            ],
        ),
    ]
