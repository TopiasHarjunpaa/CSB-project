# Generated by Django 3.1.4 on 2021-02-26 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('safebanking', '0004_auto_20210226_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_account',
            name='status',
            field=models.IntegerField(default=1),
        ),
    ]
