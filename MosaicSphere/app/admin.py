from django.contrib import admin
from .models import UploadedImage, Collage  # Ensure Collage is imported here

class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'upload_date']

# Register your models here.
admin.site.register(UploadedImage, UploadedImageAdmin)  # Use UploadedImageAdmin for UploadedImage
admin.site.register(Collage)  # Now Collage should be recognized without issues
