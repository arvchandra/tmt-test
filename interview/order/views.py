from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from interview.order.models import Order, OrderTag
from interview.order.serializers import OrderSerializer, OrderTagSerializer

# Create your views here.
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class OrderTagListCreateView(generics.ListCreateAPIView):
    queryset = OrderTag.objects.all()
    serializer_class = OrderTagSerializer


class DeactivateOrderView(APIView):
    def get(self, request, order_id):
        # Validate that order id was provided in URL
        if order_id is None:
            return Response(
                {'error': 'Order ID must be provided in the URL path.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify that order exists
        order = None
        try:
            order = Order.objects.get(pk=order_id)
        except Order.DoesNotExist:
            return Response({'error': f'There is no order with id: {order_id}.'}, status=status.HTTP_400_BAD_REQUEST)
 
        # Deactivate the order
        order.is_active = False
        order.save()

        return Response({'message': f'Order with id:{order.id} was deactivated.'}, status=status.HTTP_200_OK)
