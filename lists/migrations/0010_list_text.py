# Generated by Django 2.0.2 on 2018-04-06 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0009_auto_20180406_0708'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='text',
            field=models.TextField(default=''),
        ),
    ]