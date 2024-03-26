from django_filters import rest_framework as filters
from .models import Product


class CustomFilter(filters.FilterSet):
    created = filters.DateTimeFromToRangeFilter()
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = [
            "category",
            "user",
            "price",
            "available",
            "created",
        ]

class ProductFilter(filters.FilterSet):
    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['category', 'max_price']
