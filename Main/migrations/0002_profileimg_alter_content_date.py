# Generated by Django 4.1.5 on 2023-03-12 13:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileImg',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('user_id', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='content',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 12, 20, 43, 40, 710635)),
        ),
    ]
