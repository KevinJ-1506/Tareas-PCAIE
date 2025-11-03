# caja/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('escanear/', views.escanear_productos, name='escanear_productos'),
    path('', views.index, name='caja_index'),
    path('autoservicio/', views.punto_venta_autoservicio, name='punto_venta_autoservicio'),  # Corrige "names" por "name"
]