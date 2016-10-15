from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIRequestFactory

from users.serializers import UserSerializer
from users.auth_util import generate_token


class UserAccessTest(APITestCase):

    def setUp(self):
        bee_meta = {"email": "bee@bee.com", "first_name": "Bee",
                    "last_name": "Wayne", "password": "bee@123",
                    "address": [], "phone": []}
        bee = UserSerializer(data=bee_meta)
        bee.is_valid()
        bee.save()
        self.bee = User.objects.get(pk=bee.data['id'])

    @property
    def token(self):
        return 'JWT ' + generate_token(self.bee)['token']

    def test_unauth_get_all_users_data(self):
        response = self.client.get(reverse('userregister'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_get_all_users_data(self):
        self.bee.is_superuser = True
        self.bee.save()
        response = self.client.get(reverse(
            'userregister'), HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user_with_same_email(self):
        # Test unique constaints
        user_meta = {"email": "bee@bee.com", "first_name": "Ant",
                     "last_name": "Wayne", "password": "ant@123",
                     "address": [], "phone": []}
        response = self.client.post(reverse(
            'userregister'), data=user_meta)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(), {"error": "Unique constraint failed for column 'email'"})

    def test_user_register(self):
        user_meta = {"email": "ant@bee.com", "first_name": "Ant",
                     "last_name": "Wayne", "password": "ant@123",
                     "address": [{
                     "address": "Dum",
                     "city": "New Delhi",
                     "country": "India",
                     "pin_code": "110038",
                     "state": "Delhi"}],
                     "phone": [
                     {"country_code": "+91", "mobile_no": "9999999999"}]}
        response = self.client.post(reverse(
            'userregister'), data=user_meta)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

