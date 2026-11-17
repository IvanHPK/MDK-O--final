from django.db import models


class TypeZakazchika(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'type_zakazchika'


class Zakazchick(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    inn = models.CharField(max_length=12, blank=True, null=True)
    adres = models.CharField(max_length=200, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    type_zakazchikov = models.ForeignKey(TypeZakazchika, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'zakazchick'


class Ispolnitel(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'ispolnitel'


class Podrazdelenie(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)
    ispolnitel = models.ForeignKey(Ispolnitel, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'podrazdelenie'


class Material(models.Model):
    id = models.BigAutoField(primary_key=True)
    naimenovanie = models.CharField(max_length=100)
    edinica_izmereniya = models.CharField(max_length=30)
    cena = models.DecimalField(max_digits=16, decimal_places=5)
    kod = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'material'


class TehnologicheskayaOperaciya(models.Model):
    id = models.BigAutoField(primary_key=True)
    naimenovanie = models.CharField(max_length=150)
    edinica_izmereniya = models.CharField(max_length=30)
    cena = models.DecimalField(max_digits=16, decimal_places=5)
    norma_vremeni = models.DecimalField(max_digits=12, decimal_places=5)
    kod = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'tehnologicheskaya_operaciya'


class Specificacia(models.Model):
    id = models.BigAutoField(primary_key=True)
    naimenovanie = models.CharField(max_length=100)
    ispolnitel = models.ForeignKey(Ispolnitel, models.DO_NOTHING)
    podpis = models.CharField(max_length=100, blank=True, null=True)
    rasshifrovka_podpisi = models.CharField(max_length=150, blank=True, null=True)
    kod = models.CharField(max_length=30)

    class Meta:
        managed = False
        db_table = 'specificacia'


class SpecificaciaMaterial(models.Model):
    pk = models.CompositePrimaryKey('specificacia_id', 'material_id')
    specificacia = models.ForeignKey(Specificacia, models.DO_NOTHING)
    material = models.ForeignKey(Material, models.DO_NOTHING)
    kolichestvo = models.DecimalField(max_digits=12, decimal_places=5)

    class Meta:
        managed = False
        db_table = 'specificacia_material'


class SpecificaciaOperaciya(models.Model):
    pk = models.CompositePrimaryKey(
        'specificacia_id', 'tehnologicheskaya_operaciya_id'
    )
    specificacia = models.ForeignKey(Specificacia, models.DO_NOTHING)
    tehnologicheskaya_operaciya = models.ForeignKey(
        TehnologicheskayaOperaciya, models.DO_NOTHING
    )
    kolichestvo = models.DecimalField(max_digits=12, decimal_places=5)

    class Meta:
        managed = False
        db_table = 'specificacia_operaciya'


class ZakazPokupatela(models.Model):
    id = models.BigAutoField(primary_key=True)
    naimenovanie = models.CharField(max_length=100)
    zakazchik = models.ForeignKey(Zakazchick, models.DO_NOTHING)
    data_zakaza = models.DateField()
    summa_zakaza = models.DecimalField(max_digits=16, decimal_places=2, default=0)

    class Meta:
        managed = False
        db_table = 'zakaz_pokupatela'


class PoziciaZakaza(models.Model):
    id = models.BigAutoField(primary_key=True)
    naimenovanie = models.CharField(max_length=150)
    podrazdelenie = models.ForeignKey(Podrazdelenie, models.DO_NOTHING)
    data_zapuska = models.DateField()
    zakaz_pokupatela = models.ForeignKey(ZakazPokupatela, models.DO_NOTHING)
    specificacia = models.ForeignKey(Specificacia, models.DO_NOTHING)
    kolichestvo = models.IntegerField()
    procent_skidki = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    cena = models.DecimalField(max_digits=16, decimal_places=5)

    class Meta:
        managed = False
        db_table = 'pozicia_zakaza'