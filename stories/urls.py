from django.urls import path
from stories.views import(
    HomeView, SingleProductView,ReviewsView,ajax_variant_select,
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('singleproductview/<int:id>/', SingleProductView, name='singleproductview'),
    path('ajax_variant_select/', ajax_variant_select, name='ajax_variant_select'),
    path('reviewsview/', ReviewsView.as_view(), name='reviewsview'),
]
