from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Item
from rest_framework_simplejwt.tokens import RefreshToken

class ItemTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        
        refresh = RefreshToken.for_user(self.user)
        self.token = str(refresh.access_token)
        
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

        self.item = Item.objects.create(name="Initial Item", description="Initial Description")
        self.valid_id = self.item.id
        self.invalid_id = 999

    def test_create_item(self):
        url = reverse('item-create')
        data = {'name': 'Test Item', 'description': 'Test Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("item", response.data)

    def test_create_duplicate_item(self):
        url = reverse('item-create')
        data = {'name': self.item.name, 'description': 'Test Description'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Item already exists.')

    def test_get_existing_item(self):
        url = reverse('item-detail', kwargs={'pk': self.valid_id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.item.name)

    def test_get_nonexistent_item(self):
        url = reverse('item-detail', kwargs={'pk': self.invalid_id})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Item not found')

    def test_update_existing_item(self):
        url = reverse('item-detail', kwargs={'pk': self.valid_id})
        data = {'name': 'Updated Item', 'description': 'Updated Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Item')
        self.assertEqual(response.data['description'], 'Updated Description')

    def test_update_nonexistent_item(self):
        url = reverse('item-detail', kwargs={'pk': self.invalid_id})
        data = {'name': 'Updated Item', 'description': 'Updated Description'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Item not found')

    def test_delete_existing_item(self):
        url = reverse('item-detail', kwargs={'pk': self.valid_id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_nonexistent_item(self):
        url = reverse('item-detail', kwargs={'pk': self.invalid_id})
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Item not found')
