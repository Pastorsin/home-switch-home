# Generated by Django 2.0.8 on 2019-05-03 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('residencias', '0004_auto_20190501_2005'),
    ]

    operations = [
        migrations.RenameField(
            model_name='residencia',
            old_name='precioBase',
            new_name='precio_base',
        ),
    ]
