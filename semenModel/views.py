import json
import os

from PIL import Image, ImageEnhance
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from spermDNA.settings import BASE_DIR
from .serializers import ImageDataSerializer


# FBV - function based view
@api_view(['POST'])
def predict_view(request):
    if request.method == 'POST':
        serializer = ImageDataSerializer(data=request.data)

        if serializer.is_valid():
            try:
                serializer.save()
            except Exception as e:
                print("Error saving data", str(e))

            # there i need to call function which makes image baw - make_baw
            # make_baw()

            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        print("Request Data:", request.data)
        print("Serializer Errors:", serializer.errors)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# testing : add constants : INPUT_PATH, media_root = os.path.join(BASE_DIR, 'media/'). etc.
def make_baw():
    media_root = os.path.join(BASE_DIR, 'media/')

    input_path = media_root + 'input_images\Снимок_экрана_2023-10-06_215218.png'

    input_path = os.getcwd() + input_path
    output_path = media_root + 'baw_images/ready.png'

    img = Image.open(input_path)
    contrast = ImageEnhance.Contrast(img)
    r = contrast.enhance(1.5)
    thresh = 200

    def fn(x): return 255 if x > thresh else 0

    r = r.convert('1').point(fn, mode='1')
    r.save(fp=output_path)
    r.close()
    img.close()
