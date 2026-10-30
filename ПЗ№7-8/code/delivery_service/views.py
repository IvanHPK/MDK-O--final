from django.db import transaction
from django.db.models import Count
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView

from .models import Client, Curier, Adres, Zakaz, ZakazStatus


def home(request):
    orders = Zakaz.objects.select_related('client').order_by('-id')[:3]

    return render(
        request,
        'delivery_service/home.html',
        {'orders': orders}
    )


def stats(request):
    statuses = ZakazStatus.objects.annotate(
        order_count=Count('zakaz')
    )

    return render(request, 'delivery_service/stats.html', {
        'statuses': statuses,
        'clients_count': Client.objects.count(),
        'couriers_count': Curier.objects.count(),
        'without_status': Zakaz.objects.filter(
            zakaz_status__isnull=True
        ).count(),
    })


class OrderListView(ListView):
    model = Zakaz
    template_name = 'delivery_service/order_list.html'
    context_object_name = 'orders'
    paginate_by = 9
    ordering = ['id']

    def get_queryset(self):
        qs = super().get_queryset().select_related(
            'client',
            'curier',
            'zakaz_status',
            'address_dostavki'
        )

        q = self.request.GET.get('q', '').strip()
        status_name = self.request.GET.get('status', '')

        if q:
            qs = qs.filter(client__fio__icontains=q)

        if status_name:
            qs = qs.filter(zakaz_status__name=status_name)

        if self.request.GET.get('unassigned') == 'on':
            qs = qs.filter(curier__isnull=True)

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['statuses'] = ZakazStatus.objects.all()
        context['search_query'] = self.request.GET.get('q', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['unassigned'] = self.request.GET.get('unassigned', '')

        return context


class OrderDetailView(DetailView):
    model = Zakaz
    template_name = 'delivery_service/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return super().get_queryset().select_related(
            'client',
            'curier',
            'zakaz_status',
            'address_dostavki'
        ).prefetch_related('client__zakaz_set')


class OrderCreateView(CreateView):
    model = Zakaz
    template_name = 'delivery_service/order_form.html'

    fields = [
        'client',
        'curier',
        'address_otpravki',
        'ves',
        'summa',
        'zakaz_status',
    ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['clients'] = Client.objects.all()
        context['couriers'] = Curier.objects.all()
        context['statuses'] = ZakazStatus.objects.all()
        context['values'] = self.request.POST

        return context

    def form_valid(self, form):
        gorod = self.request.POST.get('gorod', '').strip()
        ulica = self.request.POST.get('ulica', '').strip()
        house = self.request.POST.get('house', '').strip()
        apartamen = self.request.POST.get('apartamen', '').strip()

        errors = {}

        if not form.instance.client_id:
            errors['client'] = 'Выберите клиента.'

        if not form.instance.zakaz_status_id:
            errors['zakaz_status'] = 'Выберите статус заказа.'

        if not form.instance.address_otpravki:
            errors['address_otpravki'] = 'Укажите адрес отправки.'

        if form.instance.ves is None or form.instance.ves <= 0:
            errors['ves'] = 'Вес должен быть больше нуля.'

        if form.instance.summa is None or form.instance.summa <= 0:
            errors['summa'] = 'Сумма должна быть больше нуля.'

        if not gorod or len(gorod) > 100:
            errors['gorod'] = 'Укажите город: от 1 до 100 символов.'

        if not ulica or len(ulica) > 150:
            errors['ulica'] = 'Укажите улицу: от 1 до 150 символов.'

        if not house or len(house) > 20:
            errors['house'] = 'Укажите дом: от 1 до 20 символов.'

        if len(apartamen) > 10:
            errors['apartamen'] = 'Номер квартиры: не более 10 символов.'

        if errors:
            return self.render_to_response(
                self.get_context_data(form=form, errors=errors),
                status=400
            )

        # Адрес и заказ сохраняются вместе.
        with transaction.atomic():
            form.instance.address_dostavki = Adres.objects.create(
                gorod=gorod,
                ulica=ulica,
                house=house,
                apartamen=apartamen,
            )

            return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form),
            status=400
        )

    def get_success_url(self):
        return reverse(
            'delivery_service:order_detail',
            kwargs={'pk': self.object.pk}
        )