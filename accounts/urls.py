from django.urls import path

from .views import UserSignUpView, EditProfileView, DetallePerfilView, EditarTarjetaView
from .views import AdminSignUpView, MisSubastasView, MisReservasView
from .views import ListarUsuariosView
urlpatterns = [
    path('signup/user', UserSignUpView.as_view(), name='user_signup'),
    path('signup/admin', AdminSignUpView.as_view(), name='admin_signup'),
    path('verPerfil/<int:pk>/', DetallePerfilView.as_view(), name='verPerfil'),
    path('edit/<int:pk>/', EditProfileView.as_view(), name='profile_edit'),
    path('tarjeta/<int:pk>', EditarTarjetaView.as_view(), name='editar_tarjeta'),
    path('reservas/', MisReservasView.as_view(), name='mis_reservas'),
    path('subastas/', MisSubastasView.as_view(), name='mis_subastas'),
    path('listadoUsuarios', ListarUsuariosView.as_view(), name='listadoUsuarios'),
]
