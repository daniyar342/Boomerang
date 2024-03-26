from django.urls import path
from .views import *

urlpatterns = [
    path("list/", ProductListApiView.as_view(), name="product-list"),
    path("create/", ProductCreateApiView.as_view(), name="product-create"),
    path("<int:pk>/", ProductDetailView.as_view(), name="recall-list"),
    path('<int:pk>/recall/',RecallCreateAPIView.as_view()),
    path('<int:pk>/recalls/',RecallListView.as_view()),
    path('<int:product_pk>/recall/<int:recall_pk>/', DeleteUpdateRecallView.as_view()),
    path('category/create/',CategoryCreateView.as_view()),
    path('<int:product_id>/discount/',DiscountCreateView.as_view()),
]
