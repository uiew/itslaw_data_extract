# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-08-19 08:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('itslaw', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='casedetail',
            name='court',
        ),
        migrations.AddField(
            model_name='casedetail',
            name='court',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='court', to='itslaw.LawTypes', verbose_name='审理法院'),
        ),
    ]
