from django.views.generic import TemplateView


class PremiumView(TemplateView):

    template_name = 'premium_info.html'

class AyudaView(TemplateView):
	
	template_name = 'ayuda.html'

class ContactoView(TemplateView):
	
	template_name = 'contacto.html'	