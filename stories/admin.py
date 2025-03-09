from django.contrib import admin
from unfold.admin import ModelAdmin
import admin_thumbnails

from stories.models import (
    Category,Brand,Product, Images,Color,Size,Variants,Slider,Banner,Future,Review
)
# Register your models here.
class CategoryAdmin(ModelAdmin):
    show_change_link = True
    list_display = ['id', 'parent', 'title', 'keyword', 'description', 'image_tag', 'status', 'created_date', 'updated_date']
    list_editable = ['parent',  'status']
    search_fields = ['title', 'keyword', 'description']
    list_filter = ['parent', 'status']
    readonly_fields = ['id', 'created_date', 'updated_date']
admin.site.register(Category, CategoryAdmin)

class BrandAdmin(ModelAdmin):
    show_change_link = True
    list_display = ['id', 'title', 'keyword', 'description', 'image_tag', 'status', 'created_date', 'updated_date']
    search_fields = ['title', 'keyword', 'description']
    list_filter = ['status', 'created_date', 'updated_date', 'title']
    readonly_fields = ['id', 'image_tag', 'created_date', 'updated_date']
    list_editable = ['status']
admin.site.register(Brand, BrandAdmin)

@admin_thumbnails.thumbnail('image')
class ProductImagesInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 1
    show_change_link = True

class ProductVariantsInline(admin.TabularInline):
    model = Variants
    readonly_fields = ('image_tag',)
    extra = 1
    show_change_link = True

class VariantsAdmin(ModelAdmin):
    list_display = ['id', 'product', 'title', 'color', 'size', 'image_id', 'image_tag', 'quantity', 'price', 'created_date', 'updated_date']
    list_editable = ['title', 'color', 'size', 'image_id', 'quantity', 'price']
    search_fields = ['title']
    list_filter = ['product', 'color', 'size', 'image_id', 'created_date', 'updated_date']
    readonly_fields = ['id', 'image_tag', 'created_date', 'updated_date']

admin.site.register(Variants, VariantsAdmin)

class ImagesAdmin(ModelAdmin):
    list_display = ['id', 'product', 'title', 'image_tag', 'created_date', 'updated_date']
    list_editable = ['title']
    search_fields = ['title']
    list_filter = ['product', 'created_date', 'updated_date']
    readonly_fields = ['id', 'product', 'title', 'image_tag', 'created_date', 'updated_date']

admin.site.register(Images, ImagesAdmin)

class ProductAdmin(ModelAdmin):
    inlines = [ProductImagesInline, ProductVariantsInline]  # ImagesAdmin -> ProductImagesInline
    list_display = ['id', 'category', 'brand', 'variant', 'title', 'model', 'available_in_stock_msg', 'in_stock_max', 
                    'price', 'old_price', 'discount_title', 'discount', 'offers_deadline', 'keyword', 'description', 'addition_des', 
                    'return_policy', 'is_timeline', 'deals', 'new_collection', 'latest_collection', 'pick_collection', 'girls_collection', 'men_collection', 'pc_or_laps', 'in_stock', 'status', 'created_date', 'updated_date']
    list_editable = ['category', 'brand', 'variant', 'is_timeline', 'deals', 'new_collection', 'latest_collection', 'pick_collection', 'girls_collection', 'men_collection', 'pc_or_laps', 'in_stock', 'status']
    search_fields = ['title', 'keyword', 'description']
    list_filter = ['category', 'brand', 'status', 'created_date', 'updated_date']
    readonly_fields = ['id', 'created_date', 'updated_date']

admin.site.register(Product, ProductAdmin)

class ColorAdmin(ModelAdmin):
    list_display = ['id', 'title','code','color_tag']
    list_editable = ['code']
    search_fields = ['title','code']
    list_filter = ['title','code']
    readonly_fields = ['id', 'color_tag']
admin.site.register(Color,ColorAdmin)

class SizeAdmin(ModelAdmin):
    list_display = ['id', 'title', 'code']
    list_editable = ['title', 'code']
    search_fields = ['title', 'code']
    list_filter = ['title', 'code']
    readonly_fields = ['id']
admin.site.register(Size,SizeAdmin)

class SliderAdmin(ModelAdmin):
    list_display = ['id', 'product', 'title', 'image_tag', 'created_date', 'updated_date']
    list_editable = ['title']
    search_fields = ['title']
    list_filter = ['product', 'created_date', 'updated_date']
    readonly_fields = ['id', 'image_tag', 'created_date', 'updated_date']
admin.site.register(Slider, SliderAdmin)

class BannerAdmin(ModelAdmin):
    list_display = ['id', 'product', 'title', 'image_tag', 'side_deals', 'status', 'created_date', 'updated_date']
    list_editable = ['side_deals', 'status']
    search_fields = ['title']
    list_filter = ['product', 'side_deals', 'status', 'created_date', 'updated_date']
    readonly_fields = ['id', 'image_tag', 'created_date', 'updated_date']
admin.site.register(Banner, BannerAdmin)

class FutureAdmin(ModelAdmin):
    list_display = ['id', 'product', 'title', 'hard_disk', 'cpu', 'ram', 'os', 'special_feature',  'ghaphic',  'status', 'created_date', 'updated_date']
    readonly_fields = ['id', 'created_date', 'updated_date']
    search_fields = ['title', 'hard_disk', 'cpu', 'ram', 'os', 'special_feature',  'ghaphic']
    list_filter = ['product', 'status', 'created_date', 'updated_date']
admin.site.register(Future, FutureAdmin)

class ReviewAdmin(ModelAdmin):
    list_display = ['id', 'product', 'user', 'subject','comment', 'rate', 'status','created_date', 'updated_date']
    list_editable = ['status']
    readonly_fields = ['id', 'created_date', 'updated_date']
admin.site.register(Review, ReviewAdmin)