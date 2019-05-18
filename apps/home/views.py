from django.views.generic import TemplateView
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import login, logout
from accounts.models import CustomUser


class HomePageView(TemplateView):

    template_name = 'home.html'

    def logear(self, request, username):
        login(request, CustomUser.objects.get(username=username))

    def post(self, request, *args, **kwargs):
        if 'visitante' in request.POST.keys():
            logout(request)
        elif 'estandar' in request.POST.keys():
            self.logear(request, 'mauromolina@gmail.com')
        elif 'premium' in request.POST.keys():
            self.logear(request, 'andressmilla@gmail.com')
        elif 'admin' in request.POST.keys():
            self.logear(request, 'leonelmandarino@gmail.com')

        return HttpResponseRedirect(reverse('home'))
