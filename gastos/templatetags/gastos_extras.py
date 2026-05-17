"""Filtros de template customizados."""

from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    """Retorna o valor de um dicionário pela chave. Uso: {{ dict|get_item:key }}"""
    if isinstance(dictionary, dict):
        return dictionary.get(key)
    return None
