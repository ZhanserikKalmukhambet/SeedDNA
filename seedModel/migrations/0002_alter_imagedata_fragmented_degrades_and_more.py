# Generated by Django 4.2.5 on 2023-10-05 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seedModel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagedata',
            name='fragmented_degrades',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='imagedata',
            name='fragments',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='imagedata',
            name='normals',
            field=models.IntegerField(null=True),
        ),
    ]
