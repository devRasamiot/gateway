# Generated by Django 3.2.6 on 2021-09-30 08:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logs', '0006_auto_20210930_0855'),
    ]

    operations = [
        migrations.RenameField(
            model_name='livedata',
            old_name='data',
            new_name='sensor_data',
        ),
        migrations.RenameField(
            model_name='logdata',
            old_name='data',
            new_name='sensor_data',
        ),
    ]