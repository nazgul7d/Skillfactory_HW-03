# Generated by Django 4.2.11 on 2024-04-10 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='rating',
            field=models.IntegerField(default=0),
        ),
    ]
