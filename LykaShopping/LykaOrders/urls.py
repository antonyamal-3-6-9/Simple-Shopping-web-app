
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/verify/', views.verify, name='verify'),
    path('checkout/verify/payment/<uuid:orderId>', views.payment, name='payment'),
    path('verification_denied/<uuid:orderId>', views.denied, name="denied"),
    path('checkout/payment/<uuid:orderId>/orderplaced', views.ordercompleted, name = 'ordercompleted'),
    path('myorders/', views.myorder, name = "myorder"),
    path('cancelorder/<uuid:orderId>/', views.cancelorder, name = "cancelorder"),
    path('myorders/orderdetails/<uuid:orderId>/', views.orderdetails, name='orderdetails')
]

urlpatterns= urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)