# Generated by Django 4.2.5 on 2023-10-09 12:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seedModel', '0002_alter_imagedata_fragmented_degrades_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagedata',
            name='fragmented_degrades',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='imagedata',
            name='fragments',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='imagedata',
            name='image',
            field=models.ImageField(upload_to='input_images'),
        ),
        migrations.AlterField(
            model_name='imagedata',
            name='normals',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='imagedata',
            name='percent',
            field=models.CharField(max_length=255, null=True),
        ),
    ]