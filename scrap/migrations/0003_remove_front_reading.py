# Generated by Django 4.0.3 on 2022-04-16 12:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scrap', '0002_front_delete_search'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='front',
            name='reading',
        ),
    ]
