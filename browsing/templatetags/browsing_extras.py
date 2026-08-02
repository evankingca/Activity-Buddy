from django import template
from django.utils.dateparse import parse_datetime
from django.utils import timezone

register = template.Library()

@register.filter
def prettify_list(value):
    return ", ".join(item.replace("_", " ").title() for item in value)

HOURS_LABELS = {
    '1_2': '1-2 hours/week',
    '3_4': '3-4 hours/week',
    '5_plus': '5+ hours/week',
}

@register.filter
def hours_label(value):
    return HOURS_LABELS.get(value, value)

@register.filter
def to_datetime(value):
    dt = parse_datetime(value)
    if dt and timezone.is_naive(dt):
        dt = timezone.make_aware(dt)
    return dt