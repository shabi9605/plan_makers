from django.urls import path
from .import views



urlpatterns =[
    path('payment/<int:requirement_id>',views.payment,name='payment'),
    path('payment-status', views.payment_status, name='payment-status')
]