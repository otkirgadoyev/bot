# Generated by Django 5.0.4 on 2024-06-24 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0009_alter_file_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='file',
            name='workshop_name',
        ),
        migrations.AddField(
            model_name='file',
            name='category',
            field=models.CharField(choices=[('юридический', 'юридический'), ('кадр', 'кадр'), ('бухгалтер', 'бухгалтер'), ('входящая_исходящая_почта', 'входящая исходящая почта')], max_length=100, null=True),
        ),
    ]
