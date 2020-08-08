# Generated by Django 2.2.2 on 2020-06-28 09:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0003_auto_20200628_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='connection',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='profile',
            name='follower',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.IntegerField(default=0),
        ),
    ]
