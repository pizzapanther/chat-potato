# Generated by Django 4.2.3 on 2023-07-03 20:19

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0007_auto_20230703_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='name',
            field=django.contrib.postgres.fields.citext.CICharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=django.contrib.postgres.fields.citext.CICharField(max_length=70),
        ),
        migrations.AlterUniqueTogether(
            name='room',
            unique_together={('name', 'org')},
        ),
        migrations.AlterUniqueTogether(
            name='topic',
            unique_together={('name', 'room')},
        ),
    ]
