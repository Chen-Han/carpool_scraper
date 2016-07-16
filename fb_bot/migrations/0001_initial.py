# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FbUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fb_id', models.CharField(unique=True, max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('original_title', models.CharField(default=b'', max_length=100)),
                ('url', models.CharField(unique=True, max_length=255)),
                ('scrape_date', models.DateTimeField()),
                ('phone', models.CharField(max_length=20, null=True)),
                ('from_location', models.CharField(max_length=20)),
                ('to_location', models.CharField(max_length=20)),
                ('carpool_date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Reminder',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('from_location', models.CharField(max_length=20)),
                ('to_location', models.CharField(max_length=20)),
                ('carpool_date', models.DateTimeField()),
                ('fb_user', models.ForeignKey(to='fb_bot.FbUser')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='reminder',
            unique_together=set([('fb_user', 'from_location', 'to_location', 'carpool_date')]),
        ),
    ]
