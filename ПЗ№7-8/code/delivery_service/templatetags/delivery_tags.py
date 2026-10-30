from django import template
from django.db.models import Count, Avg

from delivery_service.models import Zakaz, Curier

register = template.Library()

@register.simple_tag
def total_orders():
    return Zakaz.objects.count()


@register.simple_tag
def average_price():
    result = Zakaz.objects.aggregate(avg=Avg('summa'))
    return result['avg'] or 0


@register.inclusion_tag('delivery_service/tags/top_couriers.html')
def show_top_couriers(count=3):
    couriers = Curier.objects.annotate(
        order_count=Count('zakaz')
    ).order_by('-order_count', 'fio', 'id')[:count]

    return {'couriers': couriers}


@register.filter
def currency(value):
    try:
        return f'{float(value):.2f} ₽'
    except (ValueError, TypeError):
        return value