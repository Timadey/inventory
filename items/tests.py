from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from items.models import Item
from suppliers.models import Supplier

# Create your tests here.

class ListCreateItemViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_items(self):
        url = reverse('items')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_item(self):
        url = reverse('items')
        data = {'name': 'Test Item', 'price': '1234.99', 'description': 'Test description'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 1)  # Check if an item was created in the database

class RetrieveUpdateDestroyItemViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item = Item.objects.create(name='Test Item', price='4321.99', description='Test description')

    def test_retrieve_item(self):
        url = reverse('item', kwargs={'item': self.item.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.item.id))

    def test_update_item(self):
        url = reverse('item', kwargs={'item': self.item.id})
        updated_data = {'name': 'Updated Item Name', 'price':'2345.39', 'description': 'Updated description'}
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, 'Updated Item Name')

    def test_delete_item(self):
        url = reverse('item', kwargs={'item': self.item.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Item.objects.filter(id=self.item.id).exists())

class ItemSupplierRetrieveViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item = Item.objects.create(name='Test Item', price='4321.99', description='Test description')
        self.supplier = Supplier.objects.create(name='Test Supplier')

    def test_retrieve_item_with_suppliers(self):
        self.item.suppliers.add(self.supplier)

        url = reverse('item-supplier', kwargs={'item': self.item.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('suppliers', response.data)
        self.assertEqual(response.data['suppliers'][0]['id'], str(self.supplier.id))

class ItemSupplierRemoveViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item = Item.objects.create(name='Test Item', price='4321.99', description='Test description')
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.item.suppliers.add(self.supplier)

    def test_remove_supplier_from_item(self):
        url = reverse('item-remove-supplier', kwargs={'item': self.item.id})
        data = {'suppliers': [str(self.supplier.id)]}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.item.suppliers.filter(id=self.supplier.id).exists())
