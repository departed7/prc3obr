from django.urls import path
from . import views

app_name = 'basket'

urlpatterns = [
    # Список концертов (Афиша)
    path('', views.concert_list, name='concert_list'),
    
    # Работа с билетами (Корзина)
    path('add/<int:concert_id>/', views.basket_add, name='basket_add'),
    path('remove/<int:concert_id>/', views.basket_remove, name='basket_remove'),
    path('my-tickets/', views.basket_detail, name='basket_detail'),
    path('checkout/', views.basket_checkout, name='basket_checkout'),
]