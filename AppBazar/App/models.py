from django.db import models
from django.contrib.auth.hashers import make_password

class Cargo(models.Model):
    cod_cargo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=30)

    def __str__(self):
        return self.nombre


class Categoria(models.Model):
    cod_categoria_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Producto(models.Model):
    cod_producto = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio = models.IntegerField()
    cod_categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Cliente(models.Model):
    rut = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Usuario(models.Model):
    cod_usuario = models.AutoField(primary_key=True)
    usuario = models.CharField(max_length=100)
    contrasena = models.CharField(max_length=100)
    cod_cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE)

    def encriptar_contrasena(self, raw_password):
        self.contrasena = make_password(raw_password)

    def save(self, *args, **kwargs):
        if not self._state.adding:
            # encriptar la contraseña nuevamente si ha cambiado
            original = Usuario.objects.get(pk=self.pk)
            if original.contrasena != self.contrasena:
                self.encriptar_contrasena(self.contrasena)
        else:
            # encriptar la contraseña
            self.encriptar_contrasena(self.contrasena)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.usuario


class Tipo_venta(models.Model):
    cod_tipoventa_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Venta(models.Model):
    cod_venta = models.AutoField(primary_key=True)
    cod_usuario_id = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cod_tipoventa = models.ForeignKey(Tipo_venta, on_delete=models.CASCADE)
    rut = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    hora = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Venta {self.cod_venta}"


class Detalle_venta(models.Model):
    cod_dventa = models.AutoField(primary_key=True)
    cod_producto_id = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cod_venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    cantidad = models.IntegerField()

    def __str__(self):
        return f"Detalle venta {self.cod_dventa}"