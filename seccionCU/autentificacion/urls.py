from django.urls import path
from autentificacion import views
from autentificacion.views import VRegistro, ChangePasswordView

urlpatterns = [
    path("", views.opciones_login, name="opciones_login"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("register/", VRegistro.as_view(), name="register"),
    path("perfil/", views.perfil, name="perfil"),
    path("configuracion/", views.configuracion, name="configuracion"),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),

]