# Generated by Django 3.2.4 on 2021-06-24 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Blog', '0010_delete_postlikes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='addpost',
            old_name='like',
            new_name='likes',
        ),
    ]
