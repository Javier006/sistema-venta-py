# Generated by Django 4.1 on 2023-07-05 03:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='venta',
            name='hora',
            field=models.DateField(auto_now_add=True),
        ),
    ]