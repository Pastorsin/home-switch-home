from django.urls import path

from .views import SignUpView
from .views import DetallePerfilView


urlpatterns = [
        path('signup/', SignUpView.as_view(), name='signup'),
        path('verPerfil/<int:pk>/',
         DetallePerfilView.as_view(),
         name='verPerfil')
]
