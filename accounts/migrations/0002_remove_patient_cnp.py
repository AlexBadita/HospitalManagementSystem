# Generated by Django 3.0.5 on 2021-05-31 16:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='cnp',
        ),
    ]