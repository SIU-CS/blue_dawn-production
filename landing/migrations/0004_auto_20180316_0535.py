# Generated by Django 2.0.2 on 2018-03-16 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('landing', '0003_auto_20180316_0533'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datafile',
            name='file',
            field=models.FileField(blank=True, upload_to=''),
        ),
    ]
