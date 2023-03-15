# Generated by Django 4.1.5 on 2023-03-12 13:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Main', '0002_profileimg_alter_content_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='content',
            name='date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2023, 3, 12, 20, 55, 5, 136129)),
        ),
        migrations.AlterField(
            model_name='profileimg',
            name='image',
            field=models.ImageField(default='', upload_to='images/'),
        ),
    ]
