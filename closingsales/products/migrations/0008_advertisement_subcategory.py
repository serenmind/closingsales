# Generated by Django 2.0.5 on 2018-05-09 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_advertisement_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='advertisement',
            name='subcategory',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='products.Subcategory'),
            preserve_default=False,
        ),
    ]
