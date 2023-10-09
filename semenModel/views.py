import json

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

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
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)

        print("Request Data:", request.data)
        print("Serializer Errors:", serializer.errors)

        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def make_baw():
    pass
