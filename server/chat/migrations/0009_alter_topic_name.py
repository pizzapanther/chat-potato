# Generated by Django 4.2.3 on 2023-07-10 13:34

import django.contrib.postgres.fields.citext
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0008_alter_room_name_alter_topic_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='name',
            field=django.contrib.postgres.fields.citext.CICharField(db_index=True, max_length=70),
        ),
    ]
