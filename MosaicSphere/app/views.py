from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import UploadedImage, Collage
from PIL import Image
import datetime
import os
from django.conf import settings
from .forms import ImageUploadForm
from django.utils import timezone
from django.db.models import Max
from django.db.models.functions import TruncDay



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

    # Assuming you want a grid layout
    num_images_side = int(len(images_list) ** 0.5)  # For a square grid
    if num_images_side ** 2 < len(images_list):  # Adjust for non-perfect squares
        num_images_side += 1

    image_width, image_height = images_list[0].size
    collage_width = image_width * num_images_side
    collage_height = image_height * num_images_side

    collage = Image.new('RGB', (collage_width, collage_height))

    for index, image in enumerate(images_list):
        x = (index % num_images_side) * image_width
        y = (index // num_images_side) * image_height
        collage.paste(image, (x, y))

    # Ensure the 'collages' directory exists in your MEDIA_ROOT
    collage_directory = 'collages/'
    os.makedirs(os.path.join(settings.MEDIA_ROOT, collage_directory), exist_ok=True)
    collage_path = os.path.join(collage_directory, f'collage_{datetime.datetime.now().strftime("%Y%m%d%H%M%S")}.jpg')
    collage.save(os.path.join(settings.MEDIA_ROOT, collage_path))

    Collage.objects.create(collage_image=collage_path)

def collage(request):
    collages=Collage.objects.all()
    return render(request, 'app/collage.html', {'collages': collages})

# def hall(request):
#     collages = Collage.objects.all()
#     return render(request, 'app/hall.html', {'collages': collages})
# def hall(request):
#     # Get today's date and time
#     today = timezone.now()
#     # Calculate yesterday's date by subtracting a day from today
#     yesterday = today - datetime.timedelta(days=1)
#     # Filter collages created yesterday
#     yesterdays_collages = Collage.objects.filter(creation_date__year=yesterday.year, creation_date__month=yesterday.month, creation_date__day=yesterday.day)
#     # Get the most recent collage from yesterday
#     if yesterdays_collages.exists():
#         latest_collage = yesterdays_collages.latest('creation_date')
#         collages = [latest_collage]
#     else:
#         collages = []

#     return render(request, 'app/hall.html', {'collages': collages})
def hall(request):
    # Get the maximum 'creation_date' for each day
    dates = Collage.objects.annotate(
        date=TruncDay('creation_date')
    ).values('date').annotate(
        latest_creation=Max('creation_date')
    ).order_by('-date')

    # Now, for each date, get the corresponding latest collage
    latest_collages = []
    for date in dates:
        latest_collage = Collage.objects.filter(creation_date=date['latest_creation']).first()
        if latest_collage:
            latest_collages.append(latest_collage)

    return render(request, 'app/hall.html', {'collages': latest_collages})