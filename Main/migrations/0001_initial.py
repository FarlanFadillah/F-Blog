# Generated by Django 4.1.5 on 2023-03-12 03:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=10000)),
                ('title', models.CharField(max_length=10000)),
                ('date', models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 12, 10, 53, 36, 468668))),
                ('writer_id', models.IntegerField()),
            ],
        ),
    ]
