# Generated by Django 3.1.3 on 2020-11-13 23:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broadcasts', '0004_broadcast_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadcast',
            name='title',
            field=models.CharField(default='', max_length=100),
        ),
    ]
