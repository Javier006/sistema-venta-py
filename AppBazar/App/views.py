from datetime import date
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario, Producto, Categoria, Venta, Tipo_venta, Cliente, Detalle_venta
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect
from django.db.models import Sum, F, ExpressionWrapper ,DecimalField

def login(request):

    if request.method == 'POST':
        usuario = request.POST['username']
        password = request.POST['password']
        try:
            usuario = Usuario.objects.get(usuario=usuario)
            if check_password(password, usuario.contrasena):
                request.session['usuario_id'] = usuario.pk

                if usuario.cod_cargo_id == 1:
                    return redirect('/vendedor/?pk={}'.format(usuario.pk))
                else:
                    return redirect('/productos/?pk={}'.format(usuario.pk))
            else:
                error_message = 'Contraseña incorrecta.'
        except Usuario.DoesNotExist:
            error_message = 'El usuario no existe.'
        return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')
    


def vendedor(request):
    usuario_id = request.GET.get('pk')
    usuario_actual_id = request.session.get('usuario_id')
    venta = Venta.objects.all()
    # Obtener el usuario actual
    usuario = get_object_or_404(Usuario, cod_usuario=usuario_id)
    boleta = get_object_or_404(Tipo_venta, cod_tipoventa_id=1)
    factura = get_object_or_404(Tipo_venta, cod_tipoventa_id=2)

    if request.method == 'POST':
        rut = request.POST['rut']
        tipoboleta = request.POST.get('tipoboleta')
        tipofactura = request.POST.get('tipofactura')

        if not rut:
            rut = 0

        if Cliente.objects.filter(rut=rut).exists():
            if tipoboleta:
                tipo = tipoboleta
            elif tipofactura:
                tipo = tipofactura

            v = Venta(cod_tipoventa_id=tipo, cod_usuario_id_id=usuario_actual_id, rut_id=rut)
            v.save()
            cod_venta = v.cod_venta
            
            if tipoboleta:
                print(cod_venta)
                return redirect('/boleta/{}/'.format(cod_venta))
            elif tipofactura:
                print(cod_venta)
                return redirect('/factura/{}/'.format(cod_venta))
        else:
            c = Cliente(rut=rut, nombre='sin nombre', direccion='sin direccion')
            c.save()

            if tipoboleta:
                tipo = tipoboleta
            elif tipofactura:
                tipo = tipofactura

            v = Venta(cod_tipoventa_id=tipo, cod_usuario_id_id=usuario_actual_id, rut_id=rut)
            v.save()
            cod_venta = v.cod_venta

            if tipoboleta:
                print(cod_venta)
                return redirect('/boleta/{}/'.format(cod_venta))
            elif tipofactura:
                print(cod_venta)
                return redirect('/factura/{}/'.format(cod_venta))
    


    # Verificar la coincidencia entre los ids de usuario
    if int(usuario_id) != usuario_actual_id:
        return HttpResponseForbidden('Acceso denegado')

    return render(request, 'venta.html', {'usuario': usuario, 'venta': venta, 'boleta': boleta, 'factura': factura})
    
        
   
def informes(request):

    prueba = Venta.objects.all()

    boleta = Venta.objects.filter(cod_tipoventa_id=1)

    factura = Venta.objects.filter(cod_tipoventa_id=2)
    #sumar
    boletas = Venta.objects.filter(cod_tipoventa_id=1).annotate(total=Sum('detalle_venta__cod_producto_id__precio'))
    total_boletas = boletas.aggregate(total_boletas=Sum('total'))

    facturas = Venta.objects.filter(cod_tipoventa_id=2).annotate(total=Sum('detalle_venta__cod_producto_id__precio'))
    total_facturas = facturas.aggregate(total_facturas=Sum('total'))

    total_facturas_boletas = Venta.objects.filter(cod_tipoventa_id__in=[1, 2]).aggregate(total=Sum('detalle_venta__cod_producto_id__precio'))

    dia_actual = date.today()

    total_dia = Venta.objects.filter(hora=dia_actual).aggregate(total=Sum('detalle_venta__cod_producto_id__precio'))

    ventas = Venta.objects.all().annotate(total=Sum('detalle_venta__cod_producto_id__precio'))

    return render(request, 'planillaspdf.html',{'boleta':boleta,'factura':factura,'boletas': boletas,'facturas':facturas,'ventas': ventas,'total_boletas':total_boletas,'total_facturas':total_facturas,'total_facturas_boletas':total_facturas_boletas,'prueba':prueba,'dia_actual':dia_actual,'total_dia':total_dia})

def productos(request):
    usuario_id = int(request.GET.get('pk'))
    usuario_actual_id = request.session.get('usuario_id')

    usuario = get_object_or_404(Usuario, cod_usuario=usuario_id)

    producto = Producto.objects.all().order_by('cod_categoria_id')
    categoria = Categoria.objects.all()

    if request.method == 'POST':
        AgregarProductos(request)
        return redirect('/productos/?pk={}'.format(usuario.pk))

    if usuario_id != usuario_actual_id:
        return HttpResponseForbidden('Acceso denegado')
    

    return render(request, 'producto.html', {'producto' : producto,'categoria' : categoria,'usuario' : usuario})

def AgregarProductos(request):
   nombre = request.POST['nombre']
   categoria = request.POST['categoria']
   precio = request.POST['precio']
   cantidad = request.POST['cantidad']
   
   p = Producto(nombre=nombre,cantidad=cantidad,precio=precio,cod_categoria_id=categoria)
   p.save()

def editar(request,pk):

    usuario_actual_id = request.session.get('usuario_id')
    producto = Producto.objects.get(cod_producto=pk)
    categoria = Categoria.objects.all()

    if request.method =='POST':
        cod_producto = request.POST['id']
        nombre = request.POST['nombre']
        cod_categoria_id = request.POST['tipocategoria']
        precio = request.POST['Precio']
        cantidad = request.POST['descripcion']

        p = Producto(cod_producto,nombre,cantidad,precio,cod_categoria_id)
        p.save()
        return redirect('/productos/?pk={}'.format(usuario_actual_id))
    
    return render(request, 'editar.html',{'producto': producto,'categoria':categoria})

def boleta(request,pk):
    numeroboleta = pk
    detalle_venta = Detalle_venta.objects.filter(cod_venta_id=pk)
    rutCliente = Venta.objects.filter(cod_venta=pk)

    total_producto = Detalle_venta.objects.filter(cod_venta_id=pk).annotate(
    total=ExpressionWrapper(
        F('cod_producto_id__precio') * F('cantidad'),
        output_field=DecimalField()))

    for rut in rutCliente:
        rutcliente = rut.rut_id
    producto = Producto.objects.all()
    error_message = ''
    if request.method == 'POST':
        if request.POST.get('codigo', False):
            codigo = request.POST['codigo']
            cantidad = request.POST['cantidad']
                
            if codigo:
                if detalle_venta.filter(cod_producto_id_id = codigo).exists():
                    print("el producto ya existe")
                    cambiarCantidad = detalle_venta.filter(cod_producto_id_id = codigo)
                    for c in cambiarCantidad:
                        cambio = c.cantidad + int(cantidad)
                        if cambio > 0:
                            cod_dventa =  c.cod_dventa
                            actualizar  = Detalle_venta(cod_dventa=cod_dventa, cantidad=cambio,cod_producto_id_id=codigo, cod_venta_id = pk)
                            actualizar.save()
                        else:
                            cod_dventa =  c.cod_dventa
                            actualizar  = Detalle_venta(cod_dventa=cod_dventa, cantidad=cambio,cod_producto_id_id=codigo, cod_venta_id = pk)
                            actualizar.delete()   
                    return redirect('/boleta/{}/'.format(pk))
                elif Producto.objects.filter(cod_producto=codigo).exists():
                    producto = Producto.objects.filter(cod_producto = codigo)
                    dtall = Detalle_venta(cantidad=cantidad,cod_producto_id_id=codigo,cod_venta_id=pk)
                    dtall.save()
                    return redirect('/boleta/{}/'.format(pk))              
                else:
                    error_message = 'producto no existe'
                
    if request.POST.get('cambiarcantidad', False):
        cambiarcantidad = int(request.POST['cambiarcantidad'])
        codproducto = request.POST['producto']
        print(cambiarcantidad)

        if cambiarcantidad > 0:
            if cambiarcantidad <= 999999999:
                cambiarCantidad = detalle_venta.filter(cod_producto_id_id=codproducto)
                for c in cambiarCantidad:
                    c.cantidad = cambiarcantidad
                    c.save()
            else:
                error_message = 'La cantidad ingresada es mayor a 999999999'
        else:
            borrar = detalle_venta.filter(cod_producto_id_id=codproducto)
            borrar.delete()
   
                               
    return render(request,'boleta.html',{'detalle_venta' : detalle_venta,'producto' : producto,'error_message': error_message,'numeroboleta':numeroboleta,'rutcliente':rutcliente,'total_producto':total_producto})

def factura(request,pk):
    numerofactura = pk
    detalle_venta = Detalle_venta.objects.filter(cod_venta_id=pk)
    rutCliente = Venta.objects.filter(cod_venta=pk)

    total_producto = Detalle_venta.objects.filter(cod_venta_id=pk).annotate(
    total=ExpressionWrapper(
        F('cod_producto_id__precio') * F('cantidad'),
        output_field=DecimalField()))

    for rut in rutCliente:
        rutcliente = rut.rut_id
    producto = Producto.objects.all()
    error_message = ''
    if request.method == 'POST':
        if request.POST.get('codigo', False):
            codigo = request.POST['codigo']
            cantidad = request.POST['cantidad']
                
            if codigo:
                if detalle_venta.filter(cod_producto_id_id = codigo).exists():
                    print("el producto ya existe")
                    cambiarCantidad = detalle_venta.filter(cod_producto_id_id = codigo)
                    for c in cambiarCantidad:
                        cambio = c.cantidad + int(cantidad)
                        if cambio > 0:
                            cod_dventa =  c.cod_dventa
                            actualizar  = Detalle_venta(cod_dventa=cod_dventa, cantidad=cambio,cod_producto_id_id=codigo, cod_venta_id = pk)
                            actualizar.save()
                        else:
                            cod_dventa =  c.cod_dventa
                            actualizar  = Detalle_venta(cod_dventa=cod_dventa, cantidad=cambio,cod_producto_id_id=codigo, cod_venta_id = pk)
                            actualizar.delete()   
                    return redirect('/factura/{}/'.format(pk))
                elif Producto.objects.filter(cod_producto=codigo).exists():
                    producto = Producto.objects.filter(cod_producto = codigo)
                    dtall = Detalle_venta(cantidad=cantidad,cod_producto_id_id=codigo,cod_venta_id=pk)
                    dtall.save()
                    return redirect('/factura/{}/'.format(pk))              
                else:
                    error_message = 'producto no existe'
                
    if request.POST.get('cambiarcantidad', False):
        cambiarcantidad = int(request.POST['cambiarcantidad'])
        codproducto = request.POST['producto']
        print(cambiarcantidad)

        if cambiarcantidad > 0:
            if cambiarcantidad <= 999999999:
                cambiarCantidad = detalle_venta.filter(cod_producto_id_id=codproducto)
                for c in cambiarCantidad:
                    c.cantidad = cambiarcantidad
                    c.save()
            else:
                error_message = 'La cantidad ingresada es mayor a 999999999'
        else:
            borrar = detalle_venta.filter(cod_producto_id_id=codproducto)
            borrar.delete()
   
                               
    return render(request,'factura.html',{'detalle_venta' : detalle_venta,'producto' : producto,'error_message': error_message,'numerofactura':numerofactura,'rutcliente':rutcliente,'total_producto':total_producto})

def Eliminar(request,pk):
    detalle_venta = Detalle_venta.objects.filter(cod_dventa=pk)
    venta = Venta.objects.all()

    for v in venta:
        for d in detalle_venta:  
            if d.cod_venta_id == v.cod_venta:
                tipo = v.cod_tipoventa_id
                if tipo == 1:
                        idboleta = d.cod_venta_id
                        detalle_venta.delete()
                        return redirect('/boleta/{}/'.format(idboleta))   
                elif tipo == 2:     
                        idboleta = d.cod_venta_id
                        detalle_venta.delete()
                        return redirect('/factura/{}/'.format(idboleta))


