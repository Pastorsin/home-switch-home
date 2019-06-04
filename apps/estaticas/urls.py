from django.urls import path
from .views import PremiumView

urlpatterns = [
    path('premium', PremiumView.as_view(), name='premium_info'),
]
