# Generated by Django 2.2.2 on 2020-07-04 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userpage', '0018_auto_20200704_1023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
