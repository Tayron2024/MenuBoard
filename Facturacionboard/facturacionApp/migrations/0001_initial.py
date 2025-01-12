# Generated by Django 5.1.4 on 2025-01-11 20:50

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('correo_electronico', models.EmailField(max_length=254)),
                ('direccion', models.TextField()),
                ('telefono', models.CharField(max_length=15)),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('numero', models.AutoField(primary_key=True, serialize=False)),
                ('total', models.FloatField()),
                ('impuesto_total', models.FloatField()),
                ('descuento', models.FloatField(default=0.0)),
                ('fecha', models.DateField(default=datetime.date.today)),
            ],
        ),
        migrations.CreateModel(
            name='PagoEfectivo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_pagado', models.FloatField()),
                ('cuenta_por_cobrar', models.FloatField()),
                ('cambio', models.FloatField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PagoTarjeta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_pagado', models.FloatField()),
                ('cuenta_por_cobrar', models.FloatField()),
                ('numero_tarjeta', models.CharField(max_length=16)),
                ('titular', models.CharField(max_length=255)),
                ('vencimiento', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PagoTransferencia',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('monto_pagado', models.FloatField()),
                ('cuenta_por_cobrar', models.FloatField()),
                ('numero_transferencia', models.CharField(max_length=50)),
                ('banco_origen', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('precio', models.FloatField()),
                ('descripcion', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Promocion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.CharField(max_length=255)),
                ('porcentaje_descuento', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='HistorialDeFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('factura', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacionApp.factura')),
            ],
        ),
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('numero', models.AutoField(primary_key=True, serialize=False)),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('COMPLETADO', 'Completado'), ('CANCELADO', 'Cancelado'), ('ENPROCESO', 'En Proceso')], default='PENDIENTE', max_length=50)),
                ('fecha', models.DateField(default=datetime.date.today)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacionApp.cliente')),
            ],
        ),
        migrations.CreateModel(
            name='ItemPedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.FloatField()),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacionApp.pedido')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacionApp.producto')),
            ],
        ),
        migrations.AddField(
            model_name='factura',
            name='pedido',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='facturacionApp.pedido'),
        ),
        migrations.AddField(
            model_name='pedido',
            name='productos',
            field=models.ManyToManyField(through='facturacionApp.ItemPedido', to='facturacionApp.producto'),
        ),
    ]
