from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('',views.home, name="home"),
    path('search/', views.search, name='devSearch'),
    path('<slug:cSlug>/', views.home, name="devCat"),
    path('<slug:cSlug>/<slug:dSlug>/', views.detail, name="devDetail")
    
]
urlpatterns= urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)