# Generated by Django 4.2.15 on 2025-03-11 08:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('keyword', models.CharField(blank=True, max_length=150, null=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='brand')),
                ('status', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '02. Brands',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, unique=True)),
                ('keyword', models.CharField(blank=True, max_length=150, null=True)),
                ('description', models.CharField(blank=True, max_length=150, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='category')),
                ('status', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='stories.category')),
            ],
            options={
                'verbose_name_plural': '01. Categories',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '05.Products Colors',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant', models.CharField(choices=[('None', 'None'), ('Sizes', 'Sizes'), ('Colors', 'Colors'), ('Sizes-Colors', 'Sizes-Colors')], default='None', max_length=12)),
                ('title', models.CharField(max_length=150, unique=True)),
                ('model', models.CharField(blank=True, max_length=150, null=True)),
                ('available_in_stock_msg', models.CharField(blank=True, max_length=150, null=True)),
                ('in_stock_max', models.PositiveIntegerField(default=1)),
                ('price', models.PositiveIntegerField(default=0)),
                ('old_price', models.PositiveIntegerField(default=0)),
                ('discount_title', models.CharField(blank=True, max_length=150, null=True)),
                ('discount', models.PositiveIntegerField(default=0)),
                ('offers_deadline', models.DateTimeField(blank=True, null=True)),
                ('keyword', models.TextField(default='N/A')),
                ('description', models.TextField(default='N/A')),
                ('addition_des', models.TextField(default='N/A')),
                ('return_policy', models.TextField(default='N/A')),
                ('is_timeline', models.BooleanField(default=False)),
                ('deals', models.BooleanField(default=False)),
                ('new_collection', models.BooleanField(default=False)),
                ('latest_collection', models.BooleanField(default=False)),
                ('pick_collection', models.BooleanField(default=False)),
                ('girls_collection', models.BooleanField(default=False)),
                ('men_collection', models.BooleanField(default=False)),
                ('pc_or_laps', models.BooleanField(default=False)),
                ('in_stock', models.BooleanField(default=True)),
                ('status', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('brand', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bra_products', to='stories.brand')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cat_products', to='stories.category')),
            ],
            options={
                'verbose_name_plural': '03. Products',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('code', models.CharField(blank=True, max_length=10, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': '06. Products Sizes',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Variants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('image_id', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('price', models.PositiveIntegerField(default=0)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('color', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stories.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_variants', to='stories.product')),
                ('size', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='stories.size')),
            ],
            options={
                'verbose_name_plural': '07. Product Variants',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Slider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to='slider')),
                ('status', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='top_sliders', to='stories.product')),
            ],
            options={
                'verbose_name_plural': '08. Sliders',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=50)),
                ('comment', models.CharField(blank=True, max_length=50)),
                ('rate', models.IntegerField(default=1)),
                ('status', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '11. Reviews',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images')),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products_images', to='stories.product')),
            ],
            options={
                'verbose_name_plural': '04. Images',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Future',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150, null=True)),
                ('hard_disk', models.CharField(blank=True, max_length=150, null=True)),
                ('cpu', models.CharField(blank=True, max_length=150, null=True)),
                ('ram', models.CharField(blank=True, max_length=150, null=True)),
                ('os', models.CharField(blank=True, max_length=150, null=True)),
                ('special_feature', models.CharField(blank=True, max_length=150, null=True)),
                ('ghaphic', models.CharField(blank=True, max_length=150, null=True)),
                ('status', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='computers', to='stories.product')),
            ],
            options={
                'verbose_name_plural': '10. Future',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Banner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('image', models.ImageField(blank=True, null=True, upload_to='banners')),
                ('side_deals', models.BooleanField(default=False)),
                ('new_side', models.BooleanField(default=False)),
                ('status', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stories.product')),
            ],
            options={
                'verbose_name_plural': '09. Banners',
                'ordering': ['-id'],
            },
        ),
    ]
