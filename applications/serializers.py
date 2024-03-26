from rest_framework import serializers
from .models import Cart,Order


class CartSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cart
        fields = 'product quantity'.split()
         

class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [ "address"]

class OrderSerializerForList(serializers.ModelSerializer):
    cart_product = serializers.SerializerMethodField()  # Используйте SerializerMethodField для создания пользовательского поля

    class Meta:
        model = Order
        fields = '__all__'

    def get_cart_product(self, obj):
        # Здесь вы можете получить объект Cart и вернуть его сериализованное представление
        # Например:
        cart = obj.cart_product
        cart_serializer = CartSerializer(cart)
        return cart_serializer.data
