from django.urls import path
from .views import predict_view, test_view

urlpatterns = [
    path('predict/', predict_view),
    path('test/<int:id>/', test_view)
]