from django import template

register = template.Library()

CENSORSHIP = {
    'лопат',
    'Лопат',
    'насеко',
    'Насеко',
    'пчел',
    'Пчел'
}

@register.filter()
def censor(a):
    for word in CENSORSHIP:
        a = a.replace(word, "****")
    return a