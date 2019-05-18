from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from accounts.models import CustomUser


class HomePageView(TemplateView):

    template_name = 'home.html'

    def post(self, request, *args, **kwargs):
        # usuario = CustomUser.objects.get(username='messi')
        # login(request, usuario)
        return HttpResponseRedirect(reverse('home'))
