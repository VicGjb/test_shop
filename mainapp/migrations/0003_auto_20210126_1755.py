# Generated by Django 3.1.5 on 2021-01-26 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0002_notebook_smartphone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cardproduct',
            old_name='cart',
            new_name='card',
        ),
        migrations.RenameField(
            model_name='category',
            old_name='slaug',
            new_name='slug',
        ),
    ]
