# Generated by Django 4.2.6 on 2023-10-29 08:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('seedModel', '0008_alter_imagedata_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='imagedata',
            name='img_bytes',
        ),
    ]
