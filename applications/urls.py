from django.contrib import admin
from django.urls import path,include
from .views import OrderCreateView,CartView,CartListView,OrderAllListVIew,MyOrderView


urlpatterns = [
    path("make-order/",OrderCreateView.as_view()),
    path("add-product/",CartView.as_view()),
    path("carts/",CartListView.as_view()),
    path("order/list/",OrderAllListVIew.as_view()),
    path("my-oder/list/",MyOrderView.as_view())
]
