from django import template

register = template.Library()


@register.simple_tag
def es_seguida(semana, usuario):
    return semana.es_seguida_por(usuario)
