# Generated by Django 4.2.6 on 2023-10-18 14:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='verifyuser',
            name='verify_user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='v_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
