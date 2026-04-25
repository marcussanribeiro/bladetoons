from django import template

register = template.Library()

@register.filter
def tem_permissao(user, permissao_nome):
    if not user:
        return False
    return user.tem_permissao(permissao_nome)