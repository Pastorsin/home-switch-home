from django.urls import path
from .views import MostrarSubastaView, SemanasView, MostrarCompraDirectaView
from .views import MostrarEnEsperaView, MostrarReservadaView

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

    path('residencia/<int:pk>/semanas',
         SemanasView.as_view(),
         name='listado_semanas')
]
