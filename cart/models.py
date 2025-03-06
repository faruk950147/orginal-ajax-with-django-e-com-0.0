from django.db import models
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
from django.db.models import Avg, Count
User = get_user_model()
from stories.models import (
    Product,Variants
)

# Create your models here.
class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10, unique=True)
    coupon_discount = models.PositiveIntegerField(default=0)
    is_expired = models.BooleanField(default=False)
    minimum_amount = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '1. Coupons'     

    
    def __str__(self):
        return self.coupon_code
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    variant = models.ForeignKey(Variants, on_delete=models.CASCADE, blank=True, null=True) 
    quantity = models.PositiveIntegerField(default=1)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '01. Carts'
        
    @property
    def single_price(self):
        return (self.product.price)

    @property
    def qty_total_price(self):
        return (self.quantity * self.product.price)

    # @property
    # def Variants_price(self):
    #     return (self.quantity * self.variant.price)
    
    def __str__(self):
        return self.product.title