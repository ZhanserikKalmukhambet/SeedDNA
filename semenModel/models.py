from django.db import models


# Create your models here.

class ImageData(models.Model):
    image = models.ImageField(null=True)
    percent = models.CharField(max_length=255)
    fragments = models.IntegerField()
    fragmented_degrades = models.IntegerField()
    normals = models.IntegerField()

    class Meta:
        verbose_name = 'Image Data'
        verbose_name_plural = 'Image Data'

    def __str__(self):
        return str(self.pk)
