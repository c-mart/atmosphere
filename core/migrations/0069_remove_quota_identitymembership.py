# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-11-04 20:44
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0068_migrate_quota'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='identitymembership',
            name='quota',
        ),
        migrations.AlterField(
            model_name='identity',
            name='quota',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Quota'),
        ),
    ]
