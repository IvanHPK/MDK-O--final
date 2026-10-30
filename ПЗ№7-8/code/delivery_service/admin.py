from django.contrib import admin

from .models import (
    Adres,
    Client,
    Curier,
    CurierStatus,
    Zakaz,
    ZakazStatus,
)


admin.site.register([
    Client,
    CurierStatus,
    Curier,
    Adres,
    ZakazStatus,
    Zakaz,
])