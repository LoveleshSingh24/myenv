# Generated by Django 5.0.3 on 2024-03-16 15:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='usernmae',
            new_name='username',
        ),
    ]
