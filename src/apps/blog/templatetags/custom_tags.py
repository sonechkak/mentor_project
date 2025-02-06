# custom_tags.py
from django import template
register = template.Library()

@register.filter
def pluralize_custom(count, singular):
    if count % 10 == 1 and count % 100 != 11:  # 1 ответ
        return f"{count} {singular}"
    elif 2 <= count % 10 <= 4 and not 12 <= count % 100 <= 14:  # 2, 3, 4 ответа
        return f"{count} {singular}а"
    else:  # 0, 5-20, 22-24 и т.д. ответы
        return f"{count} {singular}ов"