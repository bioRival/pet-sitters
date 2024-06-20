from django import template

register = template.Library()

@register.filter(name='to_float')
def to_float(value):
    """
    Преобразует строку с запятой в число с плавающей точкой и возвращает строку с точкой.
    Нужно для рейтинга.
    """
    if isinstance(value, str):
        value = value.replace(',', '.')
    try:
        res = float(value)
    except:
        return value
    return "{:.1f}".format(res).replace(',', '.')