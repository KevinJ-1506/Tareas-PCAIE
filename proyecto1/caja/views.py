from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def escanear_productos(request):
    return render(request, 'caja/escanear.html')

def index(request):
    """Vista principal del módulo de caja"""
    return render(request, 'caja/index.html')

def punto_venta_autoservicio(request):
    """Vista para el punto de venta de autoservicio"""
    return render(request, 'caja/caja.html')