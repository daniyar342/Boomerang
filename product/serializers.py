from rest_framework import serializers
from .models import Category, Product, Recall, Discounts

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class RecallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recall
        fields = '__all__'

class DiscountSerializers(serializers.ModelSerializer):
    class Meta:
        model = Discounts
        fields = '__all__'
