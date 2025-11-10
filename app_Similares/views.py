from django.shortcuts import render, redirect, get_object_or_404
from .models import Cliente, Medicamento, Venta
from django.http import HttpResponse # Importa HttpResponse para casos de depuración o confirmación simple
from django.views.decorators.http import require_POST


# --- VISTAS PARA CLIENTES ---

def inicio_similares(request):
    """
    Vista para la página de inicio del sistema.
    """
    return render(request, 'app_Similares/inicio.html')

def ver_clientes(request):
    """
    Muestra una lista de todos los clientes registrados.
    """
    clientes = Cliente.objects.all().order_by('apellido', 'nombre')
    return render(request, 'app_Similares/clientes/ver_clientes.html', {'clientes': clientes})

def agregar_cliente(request):
    """
    Maneja la adición de un nuevo cliente.
    Si la solicitud es GET, muestra el formulario.
    Si la solicitud es POST, procesa los datos del formulario y guarda el cliente.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        email = request.POST.get('email')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion')
        fecha_nacimiento = request.POST.get('fecha_nacimiento')

        # Simple validación, se puede mejorar
        if nombre and apellido and email:
            # Crea un nuevo cliente
            Cliente.objects.create(
                nombre=nombre,
                apellido=apellido,
                email=email,
                telefono=telefono,
                direccion=direccion,
                fecha_nacimiento=fecha_nacimiento if fecha_nacimiento else None
            )
            return redirect('ver_clientes') # Redirige a la lista de clientes después de agregar
        else:
            # Si faltan datos importantes, puedes añadir un mensaje de error
            return render(request, 'app_Similares/clientes/agregar_clientes.html', {
                'error_message': 'Por favor, completa todos los campos obligatorios.'
            })
    return render(request, 'app_Similares/clientes/agregar_clientes.html')


def actualizar_cliente(request, pk):
    """
    Muestra el formulario para actualizar un cliente existente.
    """
    cliente = get_object_or_404(Cliente, pk=pk)
    return render(request, 'app_Similares/clientes/actualizar_clientes.html', {'cliente': cliente})

@require_POST
def realizar_actualizacion_cliente(request, pk):
    """
    Procesa los datos del formulario POST para actualizar un cliente existente.
    """
    cliente = get_object_or_404(Cliente, pk=pk)
    
    cliente.nombre = request.POST.get('nombre')
    cliente.apellido = request.POST.get('apellido')
    cliente.email = request.POST.get('email')
    cliente.telefono = request.POST.get('telefono')
    cliente.direccion = request.POST.get('direccion')
    fecha_nacimiento = request.POST.get('fecha_nacimiento')
    cliente.fecha_nacimiento = fecha_nacimiento if fecha_nacimiento else None
    
    cliente.save() # Guarda los cambios en la base de datos
    return redirect('ver_clientes') # Redirige a la lista de clientes

def borrar_cliente(request, pk):
    """
    Muestra la página de confirmación para borrar un cliente (GET)
    y luego borra el cliente si se confirma con POST.
    """
    cliente = get_object_or_404(Cliente, pk=pk)
    
    if request.method == 'POST':
        cliente.delete()
        return redirect('ver_clientes')
    
    # Si es GET, muestra la página de confirmación
    return render(request, 'app_Similares/clientes/borrar_cliente.html', {'cliente': cliente})


# --- VISTAS PARA MEDICAMENTOS ---

def ver_medicamentos(request):
    """
    Muestra una lista de todos los medicamentos registrados.
    """
    medicamentos = Medicamento.objects.all().order_by('nombre')
    return render(request, 'app_Similares/medicamentos/ver_medicamentos.html', {'medicamentos': medicamentos})


def agregar_medicamento(request):
    """
    Maneja la adición de un nuevo medicamento.
    Si la solicitud es GET, muestra el formulario.
    Si la solicitud es POST, procesa los datos del formulario y guarda el medicamento.
    """
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        laboratorio = request.POST.get('laboratorio')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        fecha_vencimiento = request.POST.get('fecha_vencimiento')
        codigo_barras = request.POST.get('codigo_barras')

        # Simple validación (sin forms.py)
        if nombre and laboratorio and precio and stock and fecha_vencimiento and codigo_barras:
            try:
                # Asegurar que precio y stock son del tipo correcto
                precio = float(precio)
                stock = int(stock)
                
                Medicamento.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    laboratorio=laboratorio,
                    precio=precio,
                    stock=stock,
                    fecha_vencimiento=fecha_vencimiento,
                    codigo_barras=codigo_barras
                )
                return redirect('ver_medicamentos')
            except ValueError:
                return render(request, 'app_Similares/medicamentos/agregar_medicamento.html', {
                    'error_message': 'Error en el formato de Precio o Stock.'
                })
        else:
            return render(request, 'app_Similares/medicamentos/agregar_medicamento.html', {
                'error_message': 'Por favor, completa todos los campos obligatorios.'
            })
    return render(request, 'app_Similares/medicamentos/agregar_medicamento.html')


def actualizar_medicamento(request, pk):
    """
    Muestra el formulario para actualizar un medicamento existente.
    """
    medicamento = get_object_or_404(Medicamento, pk=pk)
    return render(request, 'app_Similares/medicamentos/actualizar_medicamento.html', {'medicamento': medicamento})


# No se usa @require_POST si se quiere que esta vista maneje el GET también, pero aquí procesará el POST
def realizar_actualizacion_medicamento(request, pk):
    """
    Procesa los datos del formulario POST para actualizar un medicamento existente.
    """
    medicamento = get_object_or_404(Medicamento, pk=pk)
    
    if request.method == 'POST':
        medicamento.nombre = request.POST.get('nombre')
        medicamento.descripcion = request.POST.get('descripcion')
        medicamento.laboratorio = request.POST.get('laboratorio')
        medicamento.precio = request.POST.get('precio')
        medicamento.stock = request.POST.get('stock')
        medicamento.fecha_vencimiento = request.POST.get('fecha_vencimiento')
        medicamento.codigo_barras = request.POST.get('codigo_barras')
        
        try:
            medicamento.precio = float(medicamento.precio)
            medicamento.stock = int(medicamento.stock)
            medicamento.save()
            return redirect('ver_medicamentos')
        except ValueError:
            # Aquí podrías volver a renderizar el formulario con un mensaje de error
            return render(request, 'app_Similares/medicamentos/actualizar_medicamento.html', {
                'medicamento': medicamento,
                'error_message': 'Error en el formato de Precio o Stock.'
            })
    return redirect('ver_medicamentos') # Redirige si no es POST o si algo falla inesperadamente


def borrar_medicamento(request, pk):
    """
    Muestra la página de confirmación para borrar un medicamento (GET)
    y luego borra el medicamento si se confirma con POST.
    """
    medicamento = get_object_or_404(Medicamento, pk=pk)
    
    if request.method == 'POST':
        medicamento.delete()
        return redirect('ver_medicamentos')
    
    # Si es GET, muestra la página de confirmación
    return render(request, 'app_Similares/medicamentos/borrar_medicamento.html', {'medicamento': medicamento})

# --- FUNCIONES CRUD PARA VENTA ---

def agregar_venta(request):
    clientes = Cliente.objects.all()
    medicamentos = Medicamento.objects.all()

    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        medicamentos_ids = request.POST.getlist('medicamentos') # getlist para múltiples selecciones
        total = request.POST.get('total')
        metodo_pago = request.POST.get('metodo_pago')
        numero_factura = request.POST.get('numero_factura')
        observaciones = request.POST.get('observaciones')
        estado = request.POST.get('estado')

        # Obtener el objeto Cliente
        cliente_obj = get_object_or_404(Cliente, pk=cliente_id)

        nueva_venta = Venta.objects.create(
            cliente=cliente_obj,
            total=total,
            metodo_pago=metodo_pago,
            numero_factura=numero_factura,
            observaciones=observaciones,
            estado=estado,
        )
        # Asignar los medicamentos (relación ManyToMany)
        if medicamentos_ids:
            medicamentos_seleccionados = Medicamento.objects.filter(id__in=medicamentos_ids)
            nueva_venta.medicamentos.set(medicamentos_seleccionados)

        return redirect('ver_ventas') # Redirige a la lista de ventas después de agregar

    return render(request, 'venta/agregar_venta.html', {
        'clientes': clientes,
        'medicamentos': medicamentos,
        'metodos_pago': Venta.metodo_pago.field.choices,
        'estados_venta': Venta.estado.field.choices,
    })

def ver_ventas(request):
    ventas = Venta.objects.all().order_by('-fecha_venta')
    return render(request, 'venta/ver_venta.html', {'ventas': ventas})

def actualizar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    clientes = Cliente.objects.all()
    medicamentos = Medicamento.objects.all()

    if request.method == 'POST':
        venta.cliente = get_object_or_404(Cliente, pk=request.POST.get('cliente'))
        venta.total = request.POST.get('total')
        venta.metodo_pago = request.POST.get('metodo_pago')
        venta.numero_factura = request.POST.get('numero_factura')
        venta.observaciones = request.POST.get('observaciones')
        venta.estado = request.POST.get('estado')
        venta.save()

        # Actualizar medicamentos
        medicamentos_ids = request.POST.getlist('medicamentos')
        if medicamentos_ids:
            medicamentos_seleccionados = Medicamento.objects.filter(id__in=medicamentos_ids)
            venta.medicamentos.set(medicamentos_seleccionados)
        else:
            venta.medicamentos.clear() # Limpiar si no se seleccionó ninguno

        return redirect('ver_ventas')

    return render(request, 'venta/actualizar_venta.html', {
        'venta': venta,
        'clientes': clientes,
        'medicamentos': medicamentos,
        'metodos_pago': Venta.metodo_pago.field.choices,
        'estados_venta': Venta.estado.field.choices,
        'medicamentos_seleccionados': venta.medicamentos.all() # Para pre-seleccionar en el combo
    })

def borrar_venta(request, pk):
    venta = get_object_or_404(Venta, pk=pk)
    if request.method == 'POST':
        venta.delete()
        return redirect('ver_ventas')
    return render(request, 'venta/borrar_venta.html', {'venta': venta})

