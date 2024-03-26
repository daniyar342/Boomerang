from rest_framework.response import Response
from rest_framework import generics,status
from rest_framework.viewsets import GenericViewSet
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from django.db.models import Avg, Count, Q
from django_filters.rest_framework import DjangoFilterBackend
from decimal import Decimal
from .permissions import IsSellerOfProduct
from .serializers import ProductSerializer, RecallSerializer,CategorySerializer,DiscountSerializers
from .models import Product, Recall,Category,Discounts
from .filters import ProductFilter
from rest_framework import permissions
from .tasks import send_recall_to_owner


class ProductCreateApiView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductListApiView(ListAPIView):
    queryset = Product.objects.select_related('category').annotate(
        rating=Avg("recall__rating")
    )
    
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_class = ProductFilter
    ordering_fields = ['price']  
    search_fields = ['name'] 
    # permission_classes = [
    #     permissions.IsAuthenticated,
    # ]



# Представление для получения деталей, обновления и удаления продукта
class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated,]#IsSellerOfProduct]



class RecallCreateAPIView(generics.CreateAPIView):
    queryset = Recall.objects.all()
    serializer_class = RecallSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        product = Product.objects.get(pk=pk)
        product_name = product.name
        client_name = self.request.user.email_or_phone
        user_email = product.user.email_or_phone
        text = serializer.validated_data.get('text')
        serializer.save(product=product,user=self.request.user)

        """
        Клиент оставляет отзыв об этом уведомляется через email отправляется уведомление через который отправляет celery
        получает email owner of product и отправляет ему сообщение
        """
        send_recall_to_owner.delay(user_email, text,client_name,product_name)


"""
возврашает все отзывы определеноого продукта указанный
"""
class RecallListView(ListAPIView):
    queryset = Recall.objects.all()
    serializer_class = RecallSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        pk  = self.kwargs.get('pk')
        return Recall.objects.filter(product_id=pk)

    
class DeleteUpdateRecallView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Recall.objects.all()
    serializer_class = RecallSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_object(self):
        product_pk = self.kwargs.get('product_pk')
        recall_pk = self.kwargs.get('recall_pk')
        queryset = self.filter_queryset(self.get_queryset())
        obj = queryset.get(product=product_pk, pk=recall_pk)
        self.check_object_permissions(self.request, obj)
        return obj


class CategoryCreateView(generics.CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer



class DiscountCreateView(generics.CreateAPIView):
    queryset = Discounts.objects.all()
    serializer_class = DiscountSerializers

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id')
        discount_amount_str = request.data.get("discount_amount")
        discount_amount = Decimal(discount_amount_str)  # Преобразуем в Decimal
        product = Product.objects.get(pk=product_id)
        product.apply_discount(discount_amount=discount_amount)
        return super().post(request, *args, **kwargs)
    



