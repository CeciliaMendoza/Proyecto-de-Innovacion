from django.views.generic import View
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.core.paginator import Paginator
from django.core import mail
from django.utils.decorators import method_decorator
from publicaciones.forms import Crear_publicacion_form, Update_publicacion_form
from .models import Categoria, Publicaciones, Puntuacion, Solicitudes
from django.conf import settings
from django.template import Context
from django.template.loader import get_template

User = get_user_model()

# Create your views here.

@login_required
def principal(request):
    publicaciones_all = Publicaciones.objects.all().order_by("-created")
    categorias = Categoria.objects.all()
    # Show 5 contacts per page.
    paginator = Paginator(publicaciones_all, 6) 
    #obtiene el numeor de pagina 
    page_number = request.GET.get('page')
    publicaciones = paginator.get_page(page_number)

    return render(request, "publicaciones/home.html", {"publicaciones" : publicaciones, "categorias" : categorias})

@login_required
def categoria(request, categoria_id):
    categorias = Categoria.objects.all()
    #categoria seleccionada
    categoria = Categoria.objects.get(id=categoria_id)
    publicaciones_all = Publicaciones.objects.filter(categoria=categoria).order_by("-created")
    # Show 5 contacts per page.
    paginator = Paginator(publicaciones_all, 6) 
    #obtiene el numeor de pagina 
    page_number = request.GET.get('page')
    publicaciones = paginator.get_page(page_number)

    return render(request, "publicaciones/home.html", {"publicaciones" : publicaciones, "categorias" : categorias})

@login_required
def busquedas(request):
    categorias = Categoria.objects.all()
    if request.method == "GET":
        #busqueda
        query = request.GET.get('busqueda')
        #buscar sobre el campo titulo
        publicaciones_all= Publicaciones.objects.filter(titulo__contains=query).order_by("-created")
        # Show 5 contacts per page.
        paginator = Paginator(publicaciones_all, 6) 
        #obtiene el numeor de pagina 
        page_number = request.GET.get('page')
        publicaciones = paginator.get_page(page_number)
    return render(request, "publicaciones/home.html", {"publicaciones" : publicaciones, "categorias" : categorias})

@method_decorator(login_required, name='dispatch')
class crear_publicacion(View):
    def get(self, request):
        categorias = Categoria.objects.all()
        form = Crear_publicacion_form(request.POST,request.FILES)
        return render(request, "publicaciones/crear_publicacion.html", {"categorias":categorias,"form":form})
        
    def post(self, request):
        categorias = Categoria.objects.all()
        form = Crear_publicacion_form(request.POST,request.FILES)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            return redirect("perfil")
        else:
            for field, items in form.errors.items():
                for item in items:
                    messages.error(request, '{}: {}'.format(field, item))
            return render(request, "publicaciones/crear_publicacion.html", {"categorias":categorias,"form":form})

@login_required
def update_publicacion(request, publicacion_id):
    categorias = Categoria.objects.all()

    publicacion = Publicaciones.objects.get(id=publicacion_id)
    if request.method == 'POST':
        form = Update_publicacion_form(request.POST,request.FILES, instance=publicacion)
        if form.is_valid():
            form.save()
            return redirect("perfil")
    else:
        form = Update_publicacion_form(instance=publicacion)

    return render(request, "publicaciones/update_publicacion.html", {"categorias":categorias, "form": form})

@login_required
def delete_publicacion(request, publicacion_id):
    try:
        publicacion = Publicaciones.objects.get(id=publicacion_id)
        publicacion.delete()
    except Exception as e:
        print(e.message)
    return redirect("perfil")
from django.db.models import Avg

@login_required
def publicacion(request, publicacion_id):
    categorias = Categoria.objects.all()
    publicacion = Publicaciones.objects.get(id=publicacion_id)
    autor = User.objects.get(id = publicacion.autor.id)
    valoraciones_count = Puntuacion.objects.filter(publicacion=publicacion).count()
    return render(request, "publicaciones/publicacion.html", {"categorias":categorias, "publicacion": publicacion, "autor" : autor, "valoraciones_count" : valoraciones_count})

@login_required
def rate(request, publicacion_id, rating):
    post = Publicaciones.objects.get(id=publicacion_id)
    delete_row = Puntuacion.objects.filter(publicacion=post, usuario=request.user)
    delete_row.delete()
    puntuacion_row = Puntuacion.objects.create(publicacion=post, usuario=request.user, valoracion=rating)
    puntuacion_row.save()
    return redirect(publicacion, publicacion_id= publicacion_id)

@login_required
def solicitar(request, publicacion_id):
    with mail.get_connection() as connection:
        #get data
        post = Publicaciones.objects.get(id=publicacion_id)
        usuario = User.objects.get(id=request.user.id)
        #Enviar el correo
        message = get_template("publicaciones/email.html").render({
            'post': post, 'usuario' : usuario
        })
        correo = mail.EmailMessage(
            subject="Solicitud de pedido",
            body=message,
            from_email=settings.EMAIL_HOST_USER,
            to=[post.autor.email],
            reply_to=[usuario.email],
            connection=connection,
        )
        correo.content_subtype = "html"
        correo.send()
        #registro de la solicitud en la bd 
        solicitud = Solicitudes.objects.create(publicacion = post, solicitante = request.user)
        solicitud.save()
        #mensaje de exito
        messages.success(request, "Su solicitud ha sido enviada con exito!")

    return redirect(publicacion, publicacion_id= publicacion_id)


@login_required
def historial(request):
    categorias = Categoria.objects.all()
    usuario = User.objects.get(id=request.user.id)
    queryset = Solicitudes.objects.select_related('publicacion').filter(solicitante = usuario)
        
    return render(request, "publicaciones/historial_mis_solicitudes.html", {"solicitudes" : queryset, "categorias" : categorias})


@login_required
def historial_pedidos(request):
    categorias = Categoria.objects.all()
    usuario = User.objects.get(id=request.user.id)
    queryset = Solicitudes.objects.select_related('publicacion').filter(publicacion__autor = usuario)
    print(queryset)
    for q in queryset:
        print(q.solicitante.first_name)
    return render(request, "publicaciones/historial_pedidos.html", {"solicitudes" : queryset, "categorias" : categorias})