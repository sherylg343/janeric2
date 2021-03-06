# Generated by Django 3.1.5 on 2021-07-03 22:54

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_auto_20210703_2140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='created',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='product',
            name='modified',
            field=models.DateField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
