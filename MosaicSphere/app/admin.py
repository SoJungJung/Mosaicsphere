from django.contrib import admin
from .models import UploadedImage  # Adjust the import path if necessary

class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ['image', 'upload_date']  # Optional: to display fields in the admin list view

# Register your models here.
admin.site.register(UploadedImage, UploadedImageAdmin)

# Register your models here.
