# Generated by Django 5.0.8 on 2024-08-13 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='book',
            old_name='gener',
            new_name='genre',
        ),
    ]
