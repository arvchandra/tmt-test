from datetime import datetime

from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse

from interview.inventory.models import Inventory, InventoryLanguage, InventoryType
from interview.order.models import Order


class OrderDeactivateAPITest(APITestCase):

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

        # Create orders for testing
        self.initially_active_order = Order.objects.create(
            inventory=self.item_1,
            start_date=datetime.now(),
            embargo_date=datetime.now(),
            is_active=True
        )
        self.initially_inactive_order = Order.objects.create(
            inventory=self.item_1,
            start_date=datetime.now(),
            embargo_date=datetime.now(),
            is_active=False
        )

    def test_deactivate_active_order(self):
        # Generate endpoint URL
        deactivate_active_order_url = reverse(
            "deactivate-order", kwargs={"order_id": self.initially_active_order.id}
        )

        # Access the endpoint
        response = self.client.get(deactivate_active_order_url)

        # Validate status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate that order is deactivated
        validate_order = Order.objects.get(id=self.initially_active_order.id)
        self.assertEqual(validate_order.is_active, False)
        
    def test_deactivate_inactive_order(self):
        # Generate endpoint URL
        deactivate_active_order_url = reverse(
            "deactivate-order", kwargs={"order_id": self.initially_inactive_order.id}
        )

        # Access the endpoint
        response = self.client.get(deactivate_active_order_url)

        # Validate status
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Validate that order is deactivated
        validate_order = Order.objects.get(id=self.initially_inactive_order.id)
        self.assertEqual(validate_order.is_active, False)

    def test_invalid_order(self):
        # Generate endpoint URL
        deactivate_active_order_url = reverse("deactivate-order", kwargs={"order_id": 99})

        # Access the endpoint
        response = self.client.get(deactivate_active_order_url)

        # Validate that response is 400 Bad Request (order does not exist)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


