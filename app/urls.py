from django.urls import path, include
from dairyapp import views

urlpatterns = [
    # Home & Authentication
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),  # Login/Logout
    
    # Vendor URLs
    path('addvendor/', views.addvendor, name='addvendor'),
    path('add_milk_category/', views.add_milk_category, name='add_milk_category'),
    path('allvendor/', views.allvendor, name='allvendor'),
    path('ledger/<int:pk>/', views.ledger, name='ledger'),
    path('ledger_save/', views.ledger_save, name='ledger_save'),
    path('ledger_delete/', views.ledger_delete, name='ledger_delete'),
    
    # Customer URLs
    path('addcustomer/', views.addcustomer, name='addcustomer'),
    path('customer_milk_category/', views.customer_milk_category, name='customer_milk_category'),
    path('allcustomer/', views.allcustomer, name='allcustomer'),
    path('customer_ledger/<int:pk>/', views.customer_ledger, name='customer_ledger'),
    path('customer_ledger_save/', views.customer_ledger_save, name='customer_ledger_save'),
    path('customer_ledger_delete/', views.customer_ledger_delete, name='customer_ledger_delete'),
    path('Customer_page/', views.Customer_page, name='Customer_page'),
]