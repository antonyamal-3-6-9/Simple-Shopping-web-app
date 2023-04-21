from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('cartdetails/', views.displayCart, name="displaycart"),
    path('add/<int:productId>/', views.addToCart, name='add'),
    path('increment/<int:product_id>/', views.incrementItem, name='increment'),
    path('decrement/<int:product_id>/', views.decrementItem, name='decrement'),
    path('delete/<int:product_id>/', views.deleteItem, name='delete') 
]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)