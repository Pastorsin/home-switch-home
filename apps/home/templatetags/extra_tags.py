from django import template
from datetime import datetime

register = template.Library()

@register.simple_tag
def num_dia_semana():
    num_dia = datetime.today().isoweekday()
    return num_dia

@register.simple_tag
def dia_semana():
    dia_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado', 'Domingo']
    return dia_semana[num_dia_semana() - 1] # isoweekday empieza a contar desde el 1

