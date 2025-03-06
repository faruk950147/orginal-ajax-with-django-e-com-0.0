from django.shortcuts import redirect, get_object_or_404
from django.db.models import Min, Max
from django.utils import timezone
from stories.models import (
    Category, Brand, Product, Images, Color, Size, Variants,
)

def get_filters(request):
    categories = Category.objects.filter(status=True, parent=None).order_by('-id')
    cats = Category.objects.filter(status=True).order_by('-id')
    brands = Brand.objects.filter(status=True).order_by('-id')
    total_data = Product.objects.count()
    minPrice = Product.objects.all().aggregate(Min('price'))
    maxPrice = Product.objects.all().aggregate(Max('price'))
    return {
        'categories': categories,
        'cats': cats,
        'brands': brands,
        'total_data': total_data,
        'minPrice': minPrice,
        'maxPrice': maxPrice,
    }