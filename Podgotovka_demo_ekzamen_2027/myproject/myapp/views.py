from django.db import DatabaseError
from django.db.models import Sum
from django.shortcuts import render
from .models import *

def order_list(request):
    search = request.GET.get('search', '').strip()
    filter = request.GET.get('filter', '')
    field = request.GET.get('field', 'customer')
    sort = request.GET.get('sort', 'asc')
    if request.GET.get('reset'):
        filter = ''

    try:
        customers = Zakazchick.objects.order_by('name')
        orders = ZakazPokupatela.objects.select_related('zakazchik')

        if filter:
            filter = int(filter)
            orders = orders.filter(zakazchik_id=filter)

        sort_field = 'zakazchik__name'
        if field == 'date':
            sort_field = 'data_zakaza'
        if field == 'amount':
            sort_field = 'summa_zakaza'
        if sort == 'desc':
            sort_field = '-' + sort_field

        orders = orders.order_by(sort_field)
        total = orders.aggregate(total=Sum('summa_zakaza', default=0))['total']

        context = {
            'customers': customers,
            'orders': orders,
            'filter': filter,
            'search': search,
            'field': field,
            'sort': sort,
            'total': total,
        }

        error = ''
        if request.GET.get('apply_filter') and not filter:
            error = 'Выберите заказчика из списка.'
        elif request.GET.get('find') and not search:
            error = 'Введите строку поиска.'
        elif filter and not orders:
            error = 'У выбранного заказчика нет заказов.'

        if search:
            context['names'] = orders.filter(zakazchik__name__icontains=search)
            context['cities'] = orders.filter(zakazchik__adres__icontains=search)
            context['phones'] = orders.filter(zakazchik__phone__icontains=search)
            date_search = search
            parts = search.split('.')
            if len(parts) == 3:
                date_search = parts[2] + '-' + parts[1] + '-' + parts[0]
            elif len(parts) == 2:
                date_search = parts[1] + '-' + parts[0]
            context['dates'] = orders.filter(data_zakaza__icontains=date_search)
            context['amounts'] = orders.filter(
                summa_zakaza__icontains=search.replace(',', '.')
            )
            if not error and not (
                context['names'] or context['cities'] or context['phones']
                or context['dates'] or context['amounts']
            ):
                error = 'Совпадений не найдено.'
        context['error'] = error
        return render(request, 'myapp/orders.html', context)
    except (DatabaseError, ValueError):
        return render(request, 'myapp/orders.html', {
            'db_error': True,
            'error': 'Не удалось загрузить заказы. Проверьте подключение к новой базе и выбранного заказчика.',
        })