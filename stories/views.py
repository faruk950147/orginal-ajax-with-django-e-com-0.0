from django.shortcuts import render,redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.views import generic
from django.utils import timezone
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseBadRequest
from django.db.models import Min, Max
import json
from stories.models import (
    Category,Brand,Product, Images,Color,Size,Variants,Slider,Banner,Future,Review
)
from cart.forms import CartForm
#import store models

# Create your views here.
@method_decorator(never_cache, name='dispatch')
class HomeView(generic.View):
    def get(self, request):
        context = {
            'sliders': Slider.objects.filter(status=True).order_by('id'),
            'banners': Banner.objects.filter(status=True).order_by('id')[:3],
            'side_deals_banners': Banner.objects.filter(status=True, side_deals=True, new_side=True).order_by('id')[:1],
            'deals_products': Product.objects.filter(offers_deadline__isnull=False,  is_active=True, deals=True, status=True).order_by("id")[:6],
            'current_time': timezone.now(),
            'new_collections': Product.objects.filter(status=True, new_collection=True).order_by('id')[:4], 
            'girls_collections': Product.objects.filter(status=True, girls_collection=True).order_by('id')[:4],
            'men_collections': Product.objects.filter(status=True, men_collection=True).order_by('id')[:4],
            'latest_collections': Product.objects.filter(status=True, latest_collection=True).order_by('id')[:4],
            'pick_collections': Product.objects.filter(status=True, pick_collection=True).order_by('id')[:4],  
        }
        return render(request, 'stories/home.html', context)


def SingleProductView(request, id):
    # Retrieve the product by id or return a 404 error if not found
    product = get_object_or_404(Product, id=id)
    
    # Retrieve related products:
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(
        id=id
    ).select_related(
        'category'
    ).order_by('-id')[:4]
    
    # Retrieve active reviews for the product:
    reviews = Review.objects.filter(product=product, status=True).select_related('user')
    reviews_total = reviews.count()

    # Build the initial context dictionary.
    context = {
        'product': product,
        'related_products': related_products,
        'reviews': reviews,
        'reviews_total': reviews_total,
        'variant': None,  # Default variant, none selected yet.
    }

    # Check if the product has variants.
    if product.variant != 'None':
        variant = None
        
        if request.method == "POST":
            # Attempt to retrieve the selected variant using 'colorid' from the form.
            color_id = request.POST.get('colorid')
            variant = get_object_or_404(Variants, id=color_id)
            colors = Variants.objects.filter(product_id=id, size_id=variant.size_id) if variant else []
            sizes = Variants.objects.raw(
                'SELECT * FROM stories_variants WHERE product_id=%s GROUP BY size_id', [id]
            ) if variant else []
        else:
            # Retrieve all variants for the product.
            variants = list(Variants.objects.filter(product_id=id))
            
            # Check if any variants exist before trying to access the first one.
            if variants:
                # Set colors to variants that share the same size_id as the first variant.
                colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
                sizes = Variants.objects.raw(
                    'SELECT * FROM stories_variants WHERE product_id=%s GROUP BY size_id', [id]
                )
                variant = variants[0]
            else:
                # If no variants exist, fallback to empty lists and None.
                colors = []
                sizes = []
                variant = None

        # Update the context with variant-related information.
        context.update({
            'sizes': sizes,
            'colors': colors,
            'variant': variant,
        })

    return render(request, 'stories/single.html', context)


def ajax_variant_select_sizes(request):
    """ Updates the color options when Size is changed """
    if request.method == 'POST':
        productid = request.POST.get('productid')
        size_id = request.POST.get('size')

        if not productid:
            return JsonResponse({'messages': 'Invalid product ID'})

        # All variants of the product are queried only once
        variants = Variants.objects.filter(product_id=productid)

        if size_id:
            """If only Size is selected, filter colors based on the selected Size."""
            colors = variants.filter(size_id=size_id).distinct()  # Filter colors based on the selected Size

            selected_size = variants.filter(size_id=size_id).first()  # Selected size title
            selected_size_title = selected_size.size.title if selected_size else "Unknown Size"

            return JsonResponse({
                'rendered_table': render_to_string('color_list.html', {'colors': colors}),
                'size': selected_size_title
            })

    return JsonResponse({'messages': 'Invalid request'})


@method_decorator(never_cache, name='dispatch')
class ReviewsView(LoginRequiredMixin, generic.View):
    login_url = reverse_lazy('sign')
    def post(self, request):  
        if request.method == "POST":
            try:
                data = json.loads(request.body)
                # Check if updating an existing review
                review_id = data.get("review_id")  
                # Get product ID from request
                product_id = data.get("product_id")  
                # Get the form data
                subject = data.get("subject")
                comment = data.get("comment")
                rate = int(data.get("rate"))
                    
                product = get_object_or_404(Product, id=product_id)  # Ensure product exists
                    
                # Rating validation (1 to 5)
                if not (1 <= rate <= 5):
                    return JsonResponse({"status": 400, "messages": "Invalid rating. Must be between 1 and 5."})

                # Check if the user has already reviewed this product
                if not review_id:
                    existing_review = Review.objects.filter(product=product, user=request.user).first()
                    if existing_review:
                            return JsonResponse({"status": 400, "messages": "You have already reviewed this product."})
                
                if review_id:  # Editing an existing review
                    review = get_object_or_404(Review, id=review_id, user_id=request.user.id)
                    review.subject = subject
                    review.comment = comment
                    review.rate = rate
                    review.save()
                else:  # Creating a new review
                    review = Review()
                    review.product = product
                    review.user_id = request.user.id
                    review.subject = subject
                    review.comment = comment
                    review.rate = rate
                    review.save()
                return JsonResponse({
                    "status": 200,
                    "review_id": review.id,
                    "product_id": review.product.id,
                    "user": review.user.username,
                    "subject": review.subject,
                    "comment": review.comment,
                    "rate": review.rate,  
                    "updated_date": review.updated_date.strftime('%Y-%m-%d %H:%M:%S'),
                    "messages": "Review added successfully"
                })
            except Review.DoesNotExist:
                return JsonResponse({"status": 400, "messages": "Review not found for this user"})
            except Exception as e:
                return JsonResponse({"status": 400, "messages": str(e)})