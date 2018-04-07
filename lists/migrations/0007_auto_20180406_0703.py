# Generated by Django 2.0.2 on 2018-04-06 07:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0006_auto_20180406_0702'),
    ]

    operations = [
        migrations.AddField(
            model_name='list',
            name='text',
            field=models.TextField(default=''),
        ),
        migrations.AlterField(
            model_name='item',
            name='saving_list',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='lists.List'),
        ),
    ]