from django.contrib import admin
from django.urls import path
from App import views

urlpatterns =[
    path('login/', views.login),
    path('informes/', views.informes),
    path('vendedor/', views.vendedor),
    path('productos/', views.productos),
    path('agregarproductos/', views.AgregarProductos),
    path('editar/<int:pk>', views.editar),
    path('boleta/<int:pk>/', views.boleta),
    path('factura/<int:pk>/', views.factura),
    path('eliminar/<int:pk>', views.Eliminar),
]