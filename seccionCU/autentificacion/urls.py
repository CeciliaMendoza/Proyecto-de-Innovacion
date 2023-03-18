from django.urls import path
from autentificacion import views
from autentificacion.views import VRegistro, ChangePasswordView, crear_publicacion

urlpatterns = [
    path("", views.opciones_login, name="opciones_login"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", VRegistro.as_view(), name="register"),
    path("perfil/", views.perfil, name="perfil"),
    path("configuracion/", views.configuracion, name="configuracion"),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path("create/", crear_publicacion.as_view(), name="create"),
    path("delete_account/", views.delete_account, name="delete_account"),

]