# Generated by Django 3.1.4 on 2021-01-14 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safebanking', '0002_auto_20201230_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_account',
            name='motto',
            field=models.TextField(default=''),
        ),
    ]
