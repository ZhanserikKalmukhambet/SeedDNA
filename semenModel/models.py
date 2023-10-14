from django.db import models


# Create your models here.

class ImageData(models.Model):
    image = models.ImageField(upload_to='output_photos/')
    percent = models.CharField(max_length=255, null=True)
    fragments = models.FloatField(null=True)
    fragmented_degrades = models.FloatField(null=True)
    normals = models.FloatField(null=True)
    img_bytes = models.TextField(null=True)

    class Meta:
        verbose_name = 'Image Data'
        verbose_name_plural = 'Image Data'

    def __str__(self):
        return str(self.pk)
