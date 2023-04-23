from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('login/' , views.login , name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('editaddress/<int:addId>/', views.editAddress, name="editaddress"),
    path('deleteaddress/<int:addId>/', views.deleteAddress, name='deleteaddress'),
    path('addnewaddress/', views.addNewAddress, name="addnewaddress"),
    path('updatecustomer/<uuid:customerId>/', views.updateCustomer, name="update"),
    path('deletepayment/<str:paymentMethod>/<int:paymentId>/', views.deletePayment, name="deletepayment")
]

urlpatterns= urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)