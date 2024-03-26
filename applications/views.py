from rest_framework import generics
from rest_framework.response import Response
from .models import Cart, Order
from django.http import JsonResponse
from django.db import transaction
from .serializers import CartSerializer, OrderSerializer,OrderSerializerForList
from rest_framework import permissions


class CartView(generics.CreateAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartListView(generics.ListAPIView):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


    def get(self, request, *args, **kwargs):
        user = request.user
        cart = Cart.objects.get(user=user)
        serializer = self.serializer_class(cart)
        return Response(serializer.data)


class OrderCreateView(generics.CreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        try:
            user_cart = Cart.objects.get(user = self.request.user)
            serializer.save(cart_product = user_cart)
            
        except Cart.DoesNotExist:
            return JsonResponse({'error': 'У пользователя нет корзины'}, status=400)
        user_cart.delete()

class OrderAllListVIew(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializerForList


class MyOrderView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializerForList

    def get(self, request, *args, **kwargs):
        user = request.user
        orders = Order.objects.filter(cart_product__user=user)
        serializer = self.serializer_class(orders, many=True)
        return Response(serializer.data)


