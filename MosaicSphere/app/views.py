from django.shortcuts import render
from django.http import JsonResponse
from .models import UploadedImage
# from .forms import ImageUploadForm
from PIL import Image

def index(request):
    return render(request, 'app/index.html')
def main(request):
    return render(request, 'app/main.html')
def collage(request):
    return render(request, 'app/collage.html')
def hall(request):
    return render(request, 'app/hall.html')

# def upload_image(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             new_img = UploadedImage(image=request.FILES['image'])
#             new_img.save()
#             return JsonResponse({'success':True, 'msg':'Image uploaded successfully'})
#     else:
#         form = ImageUploadForm()
#     return render(request, 'index.html', {'form': form})

# def generate_collage():
#     images = [Images.open(img.image.path) for img in UploadedImage.objects.all()]
#     collage_width = 800
#     collage_height = 600
#     collage = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))
#     x_offset = 0
#     y_offset = 0
#     for img in images:
#         img.thumbnail((100,100))
#         collage.paste(img, (x_offset, y_offset))
#         x_offset += 100
#         if x_offset >= collage_width:
#             x_offset = 0
#             y_offset += 100
#     collage.save('path/to/save/collageimg')

# def view_collage(request):
#     return render(request, 'collage.html', {'collage_url':'/static/collage.jpg'})