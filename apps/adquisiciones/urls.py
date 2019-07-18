from django.urls import path
from .views import MostrarSubastaView, SemanasView, MostrarCompraDirectaView
from .views import MostrarEnEsperaView, MostrarReservadaView
from .views import MostrarHotsaleView, LeerNotificacionesView

urlpatterns = [
    path('subasta/<int:pk>/',
         MostrarSubastaView.as_view(),
         name='mostrar_subasta'),

    path('compra/<int:pk>/',
         MostrarCompraDirectaView.as_view(),
         name='mostrar_compra_directa'),

    path('espera/<int:pk>/',
         MostrarEnEsperaView.as_view(),
         name='mostrar_en_espera'),

    path('reservada/<int:pk>/',
         MostrarReservadaView.as_view(),
         name='mostrar_reservada'),

    path('hotsale/<int:pk>/',
         MostrarHotsaleView.as_view(),
         name='mostrar_hotsale'),

    path('residencia/<int:pk>/semanas',
         SemanasView.as_view(),
         name='listado_semanas'),

    path('leerNotificaciones',
         LeerNotificacionesView.as_view(),
         name='leer_notificaciones')
]
