from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from user_profiles.models import CustomUser
from django.utils.text import slugify
from decimal import Decimal
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    title = models.CharField(unique = True,max_length=50, verbose_name=_("Название"))
    slug = models.SlugField(unique=True, blank=True, verbose_name=_("Slug"))

    def save(self, *args, **kwargs):
        
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name = _("Категория")
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.title

class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name="products", on_delete=models.CASCADE, to_field='title', verbose_name=_("Категория")
    )

    user = models.ForeignKey(
        CustomUser,
        verbose_name=_("Клиент"),
        related_name="products",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    name = models.CharField(max_length=200, verbose_name=_("Название"))
    slug = models.SlugField(max_length=200, verbose_name=_("Slug"))
    description = models.TextField(blank=True, verbose_name=_("Описание"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Цена"))
    available = models.BooleanField(default=True, verbose_name=_("Доступен"))
    location = models.CharField(max_length=100, blank=True, verbose_name=_("Местоположение"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))
    
    
    def apply_discount(self, discount_amount):
        if discount_amount is not None:
            self.price -= discount_amount
            self.save()

    class Meta:
        ordering = ["name"]
        verbose_name = _("Продукт")
        verbose_name_plural = _("Продукты")
    

    def __str__(self):
        return self.name 

class ProductImage(models.Model):
    product_id = models.ForeignKey(Product,on_delete=models.CASCADE)
    image = models.ImageField(upload_to="products/%Y/%m/%d", blank=True, null=True, verbose_name=_("Изображение"))

class Recall(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name=_("Клиент"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name=_("Продукт"))
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    text = models.TextField(verbose_name=_("Текст"))
    created = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создания"))
    updated = models.DateTimeField(auto_now=True, verbose_name=_("Дата обновления"))

    class Meta:
        verbose_name = _("Отзыв")
        verbose_name_plural = _("Отзывы")

    def __str__(self):
        return f"отзыв от клиента {self.user.email_or_phone} на продукт {self.product}"





class Discounts(models.Model):
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)