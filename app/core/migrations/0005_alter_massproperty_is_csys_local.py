# Generated by Django 5.1 on 2024-08-21 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_component_skeleton_alter_component_parent_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='massproperty',
            name='is_csys_local',
            field=models.BooleanField(default=True),
        ),
    ]
