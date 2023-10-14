import base64
import logging
import os
from io import BytesIO

import torch
from PIL import Image, ImageEnhance
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse, FileResponse
from rest_framework.decorators import api_view

from .constants import INPUT_PHOTO_FOLDER_PATH, BAW_IMAGES_FOLDER_PATH, OUTPUT_PHOTO_FOLDER_PATH

logger = logging.getLogger(__name__)

model = torch.hub.load('./', 'custom', path='./model/best.pt', source='local', force_reload=True)


@api_view(['POST'])
def predict_view(request):
    cwd = os.getcwd()

    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']

        input_folder = os.path.join(cwd, INPUT_PHOTO_FOLDER_PATH)
        fs = FileSystemStorage(location=input_folder)

        try:
            saved_file_name = fs.save(uploaded_image.name, uploaded_image)
            file_url = fs.url(saved_file_name)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

        input_path = os.path.join(input_folder, saved_file_name)

        baw_folder = os.path.join(cwd, BAW_IMAGES_FOLDER_PATH)
        baw_path = os.path.join(baw_folder, saved_file_name)

        # convert input_photo to black_and_white
        make_baw(input_path=input_path, baw_path=baw_path)

        image = Image.open(baw_path)
        img_file = BytesIO()
        image.save(img_file, format='PNG')
        img_bytes = base64.b64encode(img_file.getvalue())

        data = {
            'image_url': 'https://codeforces.com/',
            'percent': '0.1%',
            'fragments': 3.14,
            'fragmented_degrades': 3.14,
            'normals': 3.14,
            'img_bytes': str(img_bytes)
        }

        return JsonResponse(data)


def make_baw(input_path, baw_path):
    global img

    try:
        img = Image.open(input_path)
    except Exception as e:
        print(str(e))

    contrast = ImageEnhance.Contrast(img)
    r = contrast.enhance(1.5)
    thresh = 200

    def fn(x):
        return 255 if x > thresh else 0

    r = r.convert('1').point(fn, mode='1')

    try:
        r.save(fp=baw_path)
    except Exception as e:
        print(str(e))

    r.close()
