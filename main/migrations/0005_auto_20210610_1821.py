# Generated by Django 2.2.5 on 2021-06-10 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20210609_1919'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadimg',
            name='pid',
            field=models.IntegerField(),
        ),
    ]
