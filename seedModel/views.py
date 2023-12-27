from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.test import TestCase

import torch, logging, os
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .constants import INPUT_PHOTO_FOLDER_PATH, BAW_IMAGES_FOLDER_PATH, OUTPUT_PHOTO_FOLDER_PATH
from .tools import make_baw, predict, get_host_name

FORMAT = '%(asctime)s %(message)s'
logging.basicConfig(format=FORMAT)
logger = logging.getLogger('logger')

model = torch.hub.load('./', 'custom', path='./model/best.pt', source='local', force_reload=True)


class PredictView(APIView):
    # permission_classes = (IsAuthenticated, )

    def post(self, request):
        cwd = os.getcwd()
        media_dir = os.path.join(cwd, 'media')

        if request.FILES['image']:
            uploaded_image = request.FILES['image']

            input_folder = os.path.join(media_dir, INPUT_PHOTO_FOLDER_PATH)
            fs = FileSystemStorage(location=input_folder)

            try:
                saved_file_name = fs.save(uploaded_image.name, uploaded_image)
                file_url = fs.url(saved_file_name)
            except Exception as e:
                logger.error(e)
                return JsonResponse({'message': str(e)}, status=400)

            input_path = os.path.join(input_folder, saved_file_name)

            baw_folder = os.path.join(media_dir, BAW_IMAGES_FOLDER_PATH)
            baw_path = os.path.join(baw_folder, saved_file_name)

            # convert input_photo to black_and_white
            make_baw(input_path=input_path, baw_path=baw_path)

            output_folder = os.path.join(media_dir, OUTPUT_PHOTO_FOLDER_PATH)
            output_path = os.path.join(output_folder, saved_file_name)

            print(output_path)

            output_data = dict(data=[], percent=0.0)
            try:
                text, output_data = predict(
                    input_model=model,
                    img_path=baw_path,
                    save_dir=output_folder,
                    data=True
                )
                logger.info('Prediction succeed!')
            except Exception as e:
                logger.error(e)
                return JsonResponse({'error': 'Occurred error, try another file'})

            relative_path = os.path.relpath(output_path, os.getcwd())
            relative_path = '/' + relative_path.replace("\\", "/")

            data = {
                'file_url': get_host_name(relative_path),
                'percent': str(round(output_data.get('percent') * 100, 2)) + '%',
                'fragments': output_data['data'][0],
                'fragmented_degradeds': output_data['data'][2],
                'normals': output_data['data'][1],
            }

            return JsonResponse(data)
