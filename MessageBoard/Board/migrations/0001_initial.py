# Generated by Django 4.2.3 on 2023-09-16 07:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('Tanks', 'Танки'), ('Healers', 'Хилы'), ('DD', 'ДД'), ('Traders', 'Торговцы'), ('Gildmasters', 'Гилдмастеры'), ('Questgivers', 'Квестгиверы'), ('Blacksmiths', 'Кузнецы'), ('Tanners', 'Кожевники'), ('PotionMakers', 'Зельевары'), ('SpellMasters', 'Мастера заклинаний')], default='Tanks', max_length=32)),
                ('message_header', models.CharField(default='', max_length=255)),
                ('message_text', models.TextField(default='')),
                ('data_create', models.DateTimeField(auto_now_add=True)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('message_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(default='')),
                ('data_create', models.DateTimeField(auto_now_add=True)),
                ('comment_status', models.IntegerField(default=2)),
                ('comment_message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='Board.message')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
