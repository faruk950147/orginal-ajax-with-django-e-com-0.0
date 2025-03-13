from django.db import models
from django.forms import ValidationError
from django.utils.html import mark_safe
from django.utils.text import slugify
from django.contrib.auth import get_user_model
import uuid
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.db.models import F, Avg, Count
User = get_user_model()



class Category(models.Model):
    parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    keyword = models.CharField(max_length=150, null=True, blank=True)  # Removed unique constraint
    description = models.CharField(max_length=150, null=True, blank=True)  # Removed unique constraint
    image = models.ImageField(upload_to='category', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '01. Categories'
        
    @property
    def image_tag(self):   
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
         # You could add a fallback image URL here if needed
        return mark_safe('<span>No Image</span>') 

    def __str__(self):
        return f'{self.title} - {"Active" if self.status else "Inactive"}'
    
class Brand(models.Model):
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    keyword = models.CharField(max_length=150, null=True, blank=True)  # Removed unique constraint
    description = models.CharField(max_length=150, null=True, blank=True)  # Removed unique constraint
    image = models.ImageField(upload_to='brand', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '02. Brands'
        
    @property
    def image_tag(self):   
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
        return mark_safe('<span>No Image</span>') 

    def __str__(self):
        return f'{self.title} - {"Active" if self.status else "Inactive"}'

class Product(models.Model):
    VARIANTS = (
        ('None', 'None'),
        ('Sizes', 'Sizes'),
        ('Colors', 'Colors'),
        ('Sizes-Colors', 'Sizes-Colors'),
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='cat_products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True, blank=True, related_name='bra_products')
    variant = models.CharField(max_length=12, choices=VARIANTS, default='None')
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    model = models.CharField(max_length=150, null=True, blank=True)
    available_in_stock_msg = models.CharField(max_length=150, null=True, blank=True)
    in_stock_max = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    old_price = models.PositiveIntegerField(default=0)
    discount_title = models.CharField(max_length=150, null=True, blank=True)
    discount = models.PositiveIntegerField(default=0)
    # Time of the off_time field
    offers_deadline  = models.DateTimeField(auto_now_add=False, blank=True, null=True)  
    keyword = models.TextField(default='N/A')
    description = models.TextField(default='N/A')
    addition_des = models.TextField(default='N/A')
    return_policy = models.TextField(default='N/A')
    is_timeline = models.BooleanField(default=False)
    deals = models.BooleanField(default=False)
    new_collection = models.BooleanField(default=False)
    latest_collection = models.BooleanField(default=False)
    pick_collection = models.BooleanField(default=False)
    girls_collection = models.BooleanField(default=False)
    men_collection = models.BooleanField(default=False)
    pc_or_laps = models.BooleanField(default=False)
    in_stock = models.BooleanField(default=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '03. Products'
        
    @property 
    def is_offers_deadline_active(self):
        return self.offers_deadline and self.offers_deadline > timezone.now()
    
    @property
    def time_remaining(self):
        """Returns the remaining time in seconds."""
        if self.offers_deadline:
            return (self.offers_deadline - timezone.now()).total_seconds()
        return None
        
    @property    
    def avaregereview(self):
        reviews = Review.objects.filter(product=self, status=True).aggregate(average=Avg('rate'))
        return float(reviews["average"] or 0)

    @property
    def countreview(self):
        return Review.objects.filter(product=self, status=True).count()
    
    def __str__(self):
        return f'{self.title} - {"Active" if self.status else "Inactive"}'
     
class Images(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products_images')
    title = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(upload_to='images', null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '04. Images'
        
    @property
    def image_tag(self):   
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50" />' % (self.image.url))
        else:
            return mark_safe('<span>No Image</span>') 
    
    def __str__(self):
        return f'{self.product.title}, {self.product.title}'
    
class Color(models.Model):
    title = models.CharField(max_length=20, unique=True, null=False, blank=False)
    code = models.CharField(max_length=20, unique=True, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '05.Products Colors'
        
    @property
    def color_tag(self):
        if self.code:
            return mark_safe('<div style="width:30px; height:30px; background-color:%s"></div>' % (self.code))
        else:
            return ""

    def __str__(self):
        return f'{self.title} x {self.code}'

class Size(models.Model):
    title = models.CharField(max_length=20, unique=True, null=False, blank=False)
    code = models.CharField(max_length=10, unique=True, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)    

    class Meta:
        ordering = ['-id']
        verbose_name_plural = '06. Products Sizes'
        
    def __str__(self):
        return f'{self.title} x {self.code}'

class Variants(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_variants')
    title = models.CharField(max_length=100, blank=True,null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL,blank=True,null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL,blank=True,null=True)
    image_id =  models.PositiveIntegerField(blank=True, null=True, default=0)
    quantity = models.PositiveIntegerField(default=1)
    price = models.PositiveIntegerField(default=0)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)    


    class Meta:
        ordering = ['-id']
        verbose_name_plural = '07. Product Variants'
        
    def __str__(self):
            return self.title if self.title else f"Variant {self.id} of {self.product.title}"
    
    @property
    def image(self):
        """Safely return the image URL or an empty string if not found."""
        try:
            img = Images.objects.get(id=self.image_id)
            return img.image.url if img.image else "No Image"
        except Images.DoesNotExist:
            return ""
    
    @property
    def image_tag(self):
        """Safely return an image tag or a placeholder if not found."""
        try:
            img = Images.objects.get(id=self.image_id)
            return mark_safe(f'<img src="{img.image.url}" width="50" height="50"/>')
        except Images.DoesNotExist:
            return mark_safe('<span>No Image</span>')

class  Slider(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='top_sliders')
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    image = models.ImageField(upload_to='slider', null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '08. Sliders'
        
    @property
    def image_tag(self):   
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
        else:
            return  mark_safe('<span>No Image</span>') 

    def __str__(self):
        return f'{self.title}'
    
class  Banner(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, unique=True, null=False, blank=False)
    image = models.ImageField(upload_to='banners', null=True, blank=True)
    side_deals = models.BooleanField(default=False)
    new_side = models.BooleanField(default=False)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '09. Banners'
        
    @property
    def image_tag(self):   
        if self.image:
            return mark_safe('<img src="%s" width="50" height="50"/>' % (self.image.url))
        else:
            return mark_safe('<span>No Image</span>') 

    def __str__(self):
        return f'{self.title}'
     
class  Future(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='computers')
    title = models.CharField(max_length=150, unique=True, null=True, blank=True)
    hard_disk = models.CharField(max_length=150, null=True, blank=True)
    cpu = models.CharField(max_length=150, null=True, blank=True)
    ram = models.CharField(max_length=150, null=True, blank=True)
    os = models.CharField(max_length=150, null=True, blank=True)
    special_feature = models.CharField(max_length=150, null=True, blank=True)
    ghaphic = models.CharField(max_length=150, null=True, blank=True)
    status = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-id']
        verbose_name_plural = '10. Future'
        
    def __str__(self):
        return self.title
    
class Review(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=50,blank=True)
    rate = models.IntegerField(default=1)
    status=models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = '11. Reviews'
        
    def __str__(self):
        return self.subject