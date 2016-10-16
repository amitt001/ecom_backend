from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from product_management.models import Product, Mobiles
from users.serializers import UserSerializer
from users.auth_util import generate_token


class ProductManagementTest(APITestCase):

    def setUp(self):
        bee_meta = {"email": "bee@bee.com", "first_name": "Bee",
                    "last_name": "Wayne", "password": "bee@123",
                    "address": [], "phone": [
                        {"country_code": "+91", "mobile_no": "9999999999"}]}
        bee = UserSerializer(data=bee_meta)
        bee.is_valid()
        bee.save()
        self.bee = User.objects.get(pk=bee.data['id'])

    @property
    def token(self):
        return 'JWT ' + generate_token(self.bee)['token']

    def _product_data(self):
        return {
            "name": "Apple IPhone 7",
            "category": "Mobiles",
            "manufacturer": "Apple",
            "price": 51000,
            "quantity": 100,
            "colour": "Gold",
            "os": "IOS",
            "memory": 32,
            "ram":"3",
            "processor": "Intel"}

    def create_product_helper(self):
        category = self._product_data()['category'].lower()
        url = reverse('categories', kwargs={"category": category})
        data = self._product_data()
        response = self.client.post(
            url, data, format='json', HTTP_AUTHORIZATION=self.token)
        _id = response.json()['id']
        return response.json(), _id, category

    def test_unauth_create_product(self):
        # Unauthorized Create product test
        category = self._product_data()['category'].lower()
        response = self.client.post(reverse(
            'categories', kwargs={"category": category}
            ), data=self._product_data())
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_product(self):
        # Successful product creation
        category = self._product_data()['category'].lower()
        url = reverse('categories', kwargs={"category": category})
        data = self._product_data()
        response = self.client.post(
            url, data, format='json', HTTP_AUTHORIZATION=self.token)
        _id = response.json()['id']
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check Product and Mobiles relation
        self.assertEqual(Mobiles.objects.first().product_id, _id)

    def test_unauth_get_category_products(self):
        # Successful category product access
        url = reverse('categories', kwargs={'category': "mobiles"})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), [])

    def test_get_product_by_id(self):
        # Anonymous product by id
        res_data, _id, category = self.create_product_helper()
        # Get product by id
        url = reverse('list_by_id', kwargs={'category': category, '_id': _id })
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_unauth_edit_product(self):
        res_data, _id, category = self.create_product_helper()
        data = self._product_data()
        updated_data = data
        updated_data['os'] = 'Android'
        url = reverse('list_by_id', kwargs={'category': category, '_id': _id })
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_product(self):
        res_data, _id, category = self.create_product_helper()
        data = self._product_data()
        updated_data = data
        updated_data['os'] = 'Android'
        url = reverse('list_by_id', kwargs={'category': category, '_id': _id })
        response = self.client.put(
            url, updated_data, format='json', HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['os'], 'Android')

    def test_unauth_delete_product(self):
        res_data, _id, category = self.create_product_helper()
        url = reverse('list_by_id', kwargs={'category': category, '_id': _id })
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_product(self):
        res_data, _id, category = self.create_product_helper()
        url = reverse('list_by_id', kwargs={'category': category, '_id': _id })
        response = self.client.delete(url, HTTP_AUTHORIZATION=self.token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_product_search(self):
        res_data, _id, category = self.create_product_helper()
        search_string = "iphone"
        url = "{}?q={}".format(
            reverse('products', kwargs={'category': category, '_id': _id }),
            search_string)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            search_string in response.data['name'].lower(), True)

    def test_product_count_offset_filter(self):
        res_data, _id, category = self.create_product_helper()
        url = "{}?start=0&offset=1".format(
            reverse('products', kwargs={'category': category, '_id': _id }))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

