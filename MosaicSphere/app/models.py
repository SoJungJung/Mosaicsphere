from django.db import models

class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploads/')
    upload_date = models.DateTimeField(auto_now_add=True)
    
class Collage(models.Model):
    collage_image = models.ImageField(upload_to='collages/')
    creation_date = models.DateField(auto_now_add=True)