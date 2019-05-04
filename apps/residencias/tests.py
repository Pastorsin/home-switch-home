from django.test import SimpleTestCase
from django.urls import reverse

# Create your tests here.


class AgregarResidenciaTest(SimpleTestCase):

    def test_agregar_residencia_status_code(self):
        response = self.client.get(reverse('agregarResidencia'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('agregarResidencia'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agregarResidencia.html')
