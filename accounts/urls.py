from django.urls import path

from .views import SignUpView, EditProfileView
from .views import DetallePerfilView, EditarTarjetaView, MisReservasView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verPerfil/<int:pk>/', DetallePerfilView.as_view(), name='verPerfil'),
    path('edit/<int:pk>/', EditProfileView.as_view(), name='profile_edit'),
    path('tarjeta/<int:pk>', EditarTarjetaView.as_view(), name='editar_tarjeta'),
    path('reservas/<int:pk>', MisReservasView.as_view(), name='mis_reservas')
]
