# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='JSONFormModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('fields', jsonfield.fields.JSONField(null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fields', jsonfield.fields.JSONField()),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('data', jsonfield.fields.JSONField()),
                ('form', models.ForeignKey(related_name=b'responses', to='django_json_form.JSONFormModel')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
