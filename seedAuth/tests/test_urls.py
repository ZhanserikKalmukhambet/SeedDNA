from django.test import SimpleTestCase
from django.urls import reverse, resolve
from ..views import RegisterView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView


# Create your tests here.


class TestUrls(SimpleTestCase):
    def test_sign_up_resolves(self):
        url = reverse('sign_up')
        self.assertEquals(resolve(url).func.view_class, RegisterView)

    def test_sign_in_resolves(self):
        url = reverse('token_obtain_pair')
        self.assertEquals(resolve(url).func.view_class, TokenObtainPairView)

    def test_sign_out_resolves(self):
        url = reverse('log_out')
        self.assertEquals(resolve(url).func.view_class, LogoutView)
