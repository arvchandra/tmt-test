from datetime import datetime

from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.utils import timezone

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType


class InventoryItemAPITest(APITestCase):

    def setUp(self):
        # Create language for testing
        self.language_1 = InventoryLanguage.objects.create(name="English")

        # Create type for testing
        self.type_1 = InventoryType.objects.create(name="Episode")

        # Create inventory items for testing
        self.item_1 = Inventory.objects.create(
            name="Simpsons Episode 1",
            language=self.language_1,
            type=self.type_1,
            metadata={}
        )
        self.item_2 = Inventory.objects.create(
            name="The Walking Dead Episode 1",
            language=self.language_1,
            type=self.type_1,
            metadata={}
        )
        self.item_3 = Inventory.objects.create(
            name="Sopranos Episode 1",
            language=self.language_1,
            type=self.type_1,
            metadata={}
        )

        naive_dt = datetime.strptime("2025-08-11", "%Y-%m-%d")

        # Create test dates
        test_date_1 = timezone.make_aware(datetime.strptime("2025-02-01", "%Y-%m-%d"))
        test_date_2 = timezone.make_aware(datetime.strptime("2025-08-11", "%Y-%m-%d"))
        test_date_3 = timezone.make_aware(datetime.strptime("2025-11-11", "%Y-%m-%d"))

        # Update created_at date for testing
        Inventory.objects.filter(pk=self.item_1.id).update(created_at=test_date_1)
        Inventory.objects.filter(pk=self.item_2.id).update(created_at=test_date_2)
        Inventory.objects.filter(pk=self.item_3.id).update(created_at=test_date_3)
        
        # Generate endpoint URL
        self.date_filter_url = reverse("inventory-date-filter")

    def test_inventory_item_filter_after_created_date(self):
        # Generate filter URL and hit the endpoint
        date_filter_url = self.date_filter_url + "?created_after=2025-07-01"
        response = self.client.get(date_filter_url)

        # Validate status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate results: 2 items should be returned (Walking Dead and Sopranos)
        self.assertEqual(len(response.data), 2)
        returned_names = [item["name"] for item in response.data]
        self.assertIn(self.item_2.name, returned_names)
        self.assertIn(self.item_3.name, returned_names)
        self.assertNotIn(self.item_1.name, returned_names)
        
    def test_inventory_item_no_created_date_in_params(self):
        # Generate filter URL without query param and hit the endpoint
        no_date_filter_url = self.date_filter_url + ""  # no query params
        
        # Assert that response has status 400
        response = self.client.get(no_date_filter_url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

