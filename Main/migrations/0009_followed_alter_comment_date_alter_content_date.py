# Generated by Django 4.1.5 on 2023-03-15 07:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0008_comment_date_alter_content_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Followed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('my_id', models.IntegerField()),
                ('followed_id', models.IntegerField()),
            ],
        ),
        migrations.AlterField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 15, 14, 12, 56, 258992)),
        ),
        migrations.AlterField(
            model_name='content',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 15, 14, 12, 56, 182681)),
        ),
    ]