# Generated by Django 5.1 on 2024-08-21 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_remove_massproperties_component'),
    ]

    operations = [
        migrations.AlterField(
            model_name='component',
            name='mass_properties',
            field=models.ManyToManyField(
                null=True,
                related_name='+',
                to='core.massproperties'
            ),
        ),
    ]
