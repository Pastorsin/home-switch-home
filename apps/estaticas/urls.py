from django.urls import path
from .views import PremiumView
from .views import AyudaView
from .views import ContactoView

urlpatterns = [
    path('premium', PremiumView.as_view(), name='premium_info'),
    path('ayuda', AyudaView.as_view(), name='ayuda'),
    path('contacto', ContactoView.as_view(), name='contacto'),
]
