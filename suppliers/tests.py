from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from items.models import Item
from suppliers.models import Supplier

# Create your tests here.
class ListCreateSupplierViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_suppliers(self):
        url = reverse('suppliers')
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_supplier(self):
        url = reverse('suppliers')
        data = {'name': 'Test Supplier'}
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Supplier.objects.count(), 1) 

class RetrieveUpdateDestroySupplierViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.supplier = Supplier.objects.create(name='Test Supplier')

    def test_retrieve_supplier(self):
        url = reverse('supplier', kwargs={'supplier': self.supplier.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], str(self.supplier.id))

    def test_update_supplier(self):
        url = reverse('supplier', kwargs={'supplier': self.supplier.id})
        updated_data = {'name': 'Updated Supplier Name'}
        response = self.client.put(url, updated_data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.supplier.refresh_from_db()
        self.assertEqual(self.supplier.name, 'Updated Supplier Name')

    def test_delete_supplier(self):
        url = reverse('supplier', kwargs={'supplier': self.supplier.id})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Supplier.objects.filter(id=self.supplier.id).exists())

class SupplierItemListCreateViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.item = Item.objects.create(name='Test Item', price='4321.99', description='Test description')

    def test_retrieve_items_for_supplier(self):
        self.supplier.items.add(self.item)

        url = reverse('supplier-item', kwargs={'supplier': self.supplier.id})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('items', response.data)
        self.assertEqual(response.data['items'][0]['id'], str(self.item.id))

    def test_update_items_for_supplier(self):
        self.supplier.items.add(self.item)

        url = reverse('supplier-item', kwargs={'supplier': self.supplier.id})
        data = {'items': [str(self.item.id)]}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.supplier.items.filter(id=self.item.id).exists())

class SupplierItemRemoveViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.supplier = Supplier.objects.create(name='Test Supplier')
        self.item = Item.objects.create(name='Test Item', price='4321.99', description='Test description')
        self.supplier.items.add(self.item)

    def test_remove_item_from_supplier(self):
        url = reverse('supplier-remove-item', kwargs={'supplier': self.supplier.id})
        data = {'items': [str(self.item.id)]}
        response = self.client.patch(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(self.supplier.items.filter(id=self.item.id).exists())
