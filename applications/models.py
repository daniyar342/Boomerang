from django.db import models
from user_profiles.models import CustomUser
from product.models import Product

class Cart(models.Model):
    user = models.ForeignKey(CustomUser,on_delete= models.CASCADE)
    product = models.ManyToManyField(Product)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default = 1)
    quantity = models.PositiveIntegerField(default = 1)
    
    class Meta:
        verbose_name = "Корзины"
        verbose_name_plural = verbose_name

    def __str__(self) -> str:
        return f"Корзина пользователя {self.user.email_or_phone}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    )
    
    date = models.DateTimeField(auto_now_add = True,verbose_name = "Дата создание заказа")   
    status = models.CharField(  max_length = 30 ,choices = STATUS_CHOICES,verbose_name = "статус заказа",)
    address = models.CharField( max_length = 50,verbose_name = "адрес заказа",)
    cart_product = models.ForeignKey(Cart, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = verbose_name

