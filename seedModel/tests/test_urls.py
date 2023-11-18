from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import PredictView


class TestUrls(SimpleTestCase):
    def test_predict_model_resolves(self):
        url = reverse('predict_model')
        print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, PredictView)




