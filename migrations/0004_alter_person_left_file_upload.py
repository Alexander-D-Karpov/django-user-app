# Generated by Django 4.0.2 on 2022-03-16 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_person_left_file_upload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='left_file_upload',
            field=models.BigIntegerField(default=0),
        ),
    ]