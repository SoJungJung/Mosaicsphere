from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UploadedImage, Collage
from PIL import Image
import datetime
import os
from django.conf import settings
from .forms import ImageUploadForm

def index(request):
    return render(request, 'app/index.html')

def main(request):
    return render(request, 'app/main.html')

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            # Call create_collage() here to generate a collage after each upload
            create_collage()
            # Redirect to the collage view instead of returning JsonResponse
            return redirect('collage')
    else:
        form = ImageUploadForm()
    return render(request, 'app/index.html', {'form': form})

def create_collage():
    images = UploadedImage.objects.all()
    if not images:
        return None  # No images to create a collage from

    images_list = [Image.open(image.image.path) for image in images]
    num_images_side = 2  # Adjust based on how many images you want per side
    image_width, image_height = images_list[0].size

    collage_width = image_width * num_images_side
    collage_height = image_height * num_images_side

    collage = Image.new('RGB', (collage_width, collage_height))

    for index, image in enumerate(images_list):
        x = index % num_images_side * image_width
        y = index // num_images_side * image_height
        collage.paste(image, (x, y))

    # Ensure the 'collages' directory exists in your MEDIA_ROOT
    collage_directory = 'collages/'
    os.makedirs(os.path.join(settings.MEDIA_ROOT, collage_directory), exist_ok=True)
    collage_path = os.path.join(collage_directory, f'collage_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.jpg')
    collage.save(os.path.join(settings.MEDIA_ROOT, collage_path))

    Collage.objects.create(collage_image=collage_path)

def collage(request):
    try:
        latest_collage = Collage.objects.latest('creation_date')
        collage_url = latest_collage.collage_image.url
    except Collage.DoesNotExist:
        collage_url = None
    return render(request, 'app/collage.html', {'collage_url': collage_url})

def hall(request):
    collages = Collage.objects.order_by('-creation_date')
    return render(request, 'app/hall.html', {'collages': collages})