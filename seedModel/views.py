import logging
import os

from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from rest_framework.decorators import api_view

import torch
from PIL import Image, ImageEnhance

from seedDNA.settings import MEDIA_URL
from .constants import INPUT_PHOTO_FOLDER_PATH, BAW_IMAGES_FOLDER_PATH, OUTPUT_PHOTO_FOLDER_PATH
from .models import ImageData
from .tools import make_baw, predict
from .serializers import ImageDataSerializer

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('logger')

model = torch.hub.load('./', 'custom', path='./model/best.pt', source='local', force_reload=True)


@api_view(['GET'])
def test_view(request, id):
    image_data = ImageData.objects.get(pk=id)

    serializer = ImageDataSerializer(image_data, context={'request': request})

    return JsonResponse(serializer.data)


@api_view(['POST'])
def predict_view(request):
    cwd = os.getcwd()

    media_dir = os.path.join(cwd, 'media')

    if request.method == 'POST' and request.FILES['image']:
        uploaded_image = request.FILES['image']

        input_folder = os.path.join(media_dir, INPUT_PHOTO_FOLDER_PATH)
        fs = FileSystemStorage(location=input_folder)

        try:
            saved_file_name = fs.save(uploaded_image.name, uploaded_image)
            file_url = fs.url(saved_file_name)
        except Exception as e:
            return JsonResponse({'message': str(e)}, status=400)

        input_path = os.path.join(input_folder, saved_file_name)

        baw_folder = os.path.join(media_dir, BAW_IMAGES_FOLDER_PATH)
        baw_path = os.path.join(baw_folder, saved_file_name)

        # convert input_photo to black_and_white
        make_baw(input_path=input_path, baw_path=baw_path)

        output_data = dict(data=[], percent=0.0)
        try:
            text, output_data = predict(
                input_model=model,
                img_path=baw_path,
                save_dir=os.path.join(media_dir, OUTPUT_PHOTO_FOLDER_PATH),
                data=True
            )
            logger.info('Prediction succeed!')
        except Exception as e:
            logger.error(e)
            return JsonResponse({'error': 'Occurred error, try another file'})

        data = {
            'file_url': 'it have to be changed !',
            'percent': str(round(output_data.get('percent') * 100, 2)) + '%',
            'fragments': output_data['data'][0],
            'fragmented_degradeds': output_data['data'][2],
            'normals': output_data['data'][1],
        }

        return JsonResponse(data)
