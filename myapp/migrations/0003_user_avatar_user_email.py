# Generated by Django 4.2.19 on 2025-02-25 15:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.URLField(blank=True, help_text='头像URL', max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, help_text='邮箱', max_length=100, null=True),
        ),
    ]
