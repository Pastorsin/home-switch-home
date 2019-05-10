from django.urls import path
from .views import MostrarSubastaView

urlpatterns = [
    path('subasta/<int:pk>/',
         MostrarSubastaView.as_view(),
         name='mostrar_subasta')
]
