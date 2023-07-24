from django.contrib import admin
from .models import Detalle_venta,Venta,Tipo_venta,Cliente,Producto,Categoria,Usuario,Cargo

# Register your models here.


admin.site.register(Detalle_venta)

admin.site.register(Venta)

admin.site.register(Tipo_venta)

admin.site.register(Cliente)

admin.site.register(Producto)

admin.site.register(Categoria)

admin.site.register(Usuario)

admin.site.register(Cargo)