from django.db import models


class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    fio = models.CharField(
        'ФИО', max_length=150, blank=True, null=True
    )
    phone = models.CharField(
        'Телефон', max_length=20, blank=True, null=True
    )
    adres = models.CharField(
        'Адрес клиента', max_length=255, blank=True, null=True
    )

    class Meta:
        db_table = 'client'
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        ordering = ['fio']

    def __str__(self):
        return self.fio or f'Клиент №{self.pk}'


class CurierStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        'Название', max_length=50, blank=True, null=True
    )

    class Meta:
        db_table = 'curier_status'
        verbose_name = 'Статус курьера'
        verbose_name_plural = 'Статусы курьеров'
        ordering = ['name']

    def __str__(self):
        return self.name or f'Статус курьера №{self.pk}'


class Curier(models.Model):
    id = models.BigAutoField(primary_key=True)
    fio = models.CharField(
        'ФИО', max_length=150, blank=True, null=True
    )
    phone = models.CharField(
        'Телефон', max_length=20, blank=True, null=True
    )
    raion = models.CharField(
        'Район', max_length=100, blank=True, null=True
    )
    curier_status = models.ForeignKey(
        CurierStatus,
        on_delete=models.DO_NOTHING,
        verbose_name='Статус курьера',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'curier'
        verbose_name = 'Курьер'
        verbose_name_plural = 'Курьеры'
        ordering = ['fio']

    def __str__(self):
        return self.fio or f'Курьер №{self.pk}'


class Adres(models.Model):
    id = models.BigAutoField(primary_key=True)
    gorod = models.CharField(
        'Город', max_length=100, blank=True, null=True
    )
    ulica = models.CharField(
        'Улица', max_length=150, blank=True, null=True
    )
    house = models.CharField(
        'Дом', max_length=20, blank=True, null=True
    )
    apartamen = models.CharField(
        'Квартира', max_length=10, blank=True, null=True
    )

    class Meta:
        db_table = 'adres'
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'
        ordering = ['gorod', 'ulica', 'house']

    def __str__(self):
        address = (
            f'{self.gorod or ""}, '
            f'{self.ulica or ""}, '
            f'д. {self.house or ""}'
        )
        if self.apartamen:
            address += f', кв. {self.apartamen}'
        return address


class ZakazStatus(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(
        'Название', max_length=50, blank=True, null=True
    )

    class Meta:
        db_table = 'zakaz_status'
        verbose_name = 'Статус заказа'
        verbose_name_plural = 'Статусы заказов'
        ordering = ['name']

    def __str__(self):
        return self.name or f'Статус заказа №{self.pk}'


class Zakaz(models.Model):
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(
        Client,
        on_delete=models.DO_NOTHING,
        verbose_name='Клиент',
        blank=True,
        null=True,
    )
    curier = models.ForeignKey(
        Curier,
        on_delete=models.DO_NOTHING,
        verbose_name='Курьер',
        blank=True,
        null=True,
    )
    address_otpravki = models.CharField(
        'Адрес отправки',
        max_length=255,
        blank=True,
        null=True,
    )
    address_dostavki = models.OneToOneField(
        Adres,
        on_delete=models.DO_NOTHING,
        verbose_name='Адрес доставки',
        blank=True,
        null=True,
    )
    ves = models.DecimalField(
        'Вес, кг',
        max_digits=7,
        decimal_places=2,
        blank=True,
        null=True,
    )
    summa = models.DecimalField(
        'Сумма, руб.',
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )
    zakaz_status = models.ForeignKey(
        ZakazStatus,
        on_delete=models.DO_NOTHING,
        verbose_name='Статус заказа',
        blank=True,
        null=True,
    )

    class Meta:
        db_table = 'zakaz'
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'
        ordering = ['id']

    def __str__(self):
        return f'Заказ №{self.pk}'