import json
import os

from PIL import Image, ImageEnhance
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.template.defaulttags import csrf_token
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from spermDNA import settings
from spermDNA.settings import BASE_DIR
from .serializers import ImageDataSerializer
from .constants import INPUT_PHOTO_FOLDER_PATH, BAW_IMAGES_FOLDER_PATH


@api_view(['POST'])
def predict_view(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']

        input_folder = os.path.join(settings.MEDIA_ROOT, INPUT_PHOTO_FOLDER_PATH)
        fs = FileSystemStorage(location=input_folder)

        try:
            saved_file = fs.save(uploaded_image.name, uploaded_image)
            file_url = fs.url(saved_file)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

        input_path = os.path.join(input_folder, saved_file)

        baw_folder = os.path.join(settings.MEDIA_ROOT, BAW_IMAGES_FOLDER_PATH)
        baw_path = os.path.join(baw_folder, saved_file)

        make_baw(input_path=input_path, baw_path=baw_path)

        return JsonResponse({'message': 'Image saved successfully', 'file_url': file_url})


def make_baw(input_path, baw_path):
    global img

    try:
        img = Image.open(input_path)
    except Exception as e:
        print(str(e))

    contrast = ImageEnhance.Contrast(img)
    r = contrast.enhance(1.5)
    thresh = 200

    def fn(x): return 255 if x > thresh else 0

    r = r.convert('1').point(fn, mode='1')

    try:
        r.save(fp=baw_path)
    except Exception as e:
        print(str(e))

    r.close()
