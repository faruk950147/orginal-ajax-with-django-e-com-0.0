from django.urls import path
from stories.views import(
    HomeView, SingleProductView,ReviewsView,ajax_variant_select_sizes,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('singleproductview/<int:id>/', SingleProductView, name='singleproductview'),
    path('ajax_variant_select_sizes/', ajax_variant_select_sizes, name='ajax_variant_select_sizes'),
    path('reviewsview/', ReviewsView.as_view(), name='reviewsview'),
]
