# Generated by Django 2.0.5 on 2018-05-15 15:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0012_adimage'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advertisement',
            name='image',
        ),
    ]
