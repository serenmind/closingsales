# Generated by Django 2.0.5 on 2018-05-29 07:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0016_auto_20180529_0710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adimage',
            name='file',
            field=models.ImageField(upload_to='advertisements'),
        ),
    ]
