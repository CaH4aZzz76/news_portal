from django import template
import re

register = template.Library()

BAD_WORDS = ['жопа', 'дебил', 'дурак', 'лох', 'дерьмо']

@register.filter
def censor(value):
    for word in BAD_WORDS:
        pattern = re.compile(re.escape(word), re.IGNORECASE)
        value = pattern.sub('*' * len(word), value)
    return value