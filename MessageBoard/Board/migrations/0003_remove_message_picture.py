# Generated by Django 4.2.3 on 2023-09-18 01:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Board', '0002_alter_comment_comment_message_alter_comment_user_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='picture',
        ),
    ]
