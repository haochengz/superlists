# Generated by Django 2.0.2 on 2018-04-14 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0011_auto_20180406_0718'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ('id',)},
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('saving_list', 'text')},
        ),
    ]
