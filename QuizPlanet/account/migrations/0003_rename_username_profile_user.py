# Generated by Django 5.0.3 on 2024-03-16 15:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_rename_usernmae_profile_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='username',
            new_name='user',
        ),
    ]