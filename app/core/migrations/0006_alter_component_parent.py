# Generated by Django 5.1 on 2024-08-21 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_massproperty_is_csys_local'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='parent',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
