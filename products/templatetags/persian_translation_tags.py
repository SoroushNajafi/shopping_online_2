from django import template
from django.utils.translation import get_language


register = template.Library()


@register.filter
def translate_number(value):
    value = str(value)
    current_lang = get_language()
    if current_lang == 'fa':
        eng_to_per_table = value.maketrans('0123456789', '۰١٢٣٤٥٦٧٨٩')
        return value.translate(eng_to_per_table)
    else:
        pers_to_eng_table = value.maketrans('۰١٢٣٤٥٦٧٨٩', '0123456789')
        return value.translate(pers_to_eng_table)
