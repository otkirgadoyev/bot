# Generated by Django 5.0.4 on 2024-06-07 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0007_alter_file_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telegram_id',
            field=models.CharField(max_length=15, null=True, verbose_name='Telegram id'),
        ),
    ]
