# Generated by Django 3.1 on 2022-03-10 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prediction', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='title',
            field=models.CharField(default='img', max_length=100),
        ),
    ]