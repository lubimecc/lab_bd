from django.db import models


# Create your models here.
class Flats(models.Model):
    flat_id = models.AutoField(primary_key=True)
    flat_number = models.IntegerField()

    def __str__(self):
        return str(self.flat_number)


class Charges(models.Model):
    charge_id = models.AutoField(primary_key=True, null=False)
    charge_amount = models.FloatField()
    flat = models.ForeignKey(Flats, on_delete=models.CASCADE)
    datetime = models.DateTimeField(null=False)


class Payments(models.Model):
    payment_id = models.AutoField(primary_key=True, null=False)
    payment_amount = models.FloatField(default=1)
    flat = models.ForeignKey(Flats, on_delete=models.CASCADE)
    datetime = models.DateTimeField(null=False)


class Saldo(models.Model):
    saldo_id = models.AutoField(primary_key=True, null=False)
    saldo_amount = models.FloatField()
    flat = models.IntegerField()
    datetime = models.DateTimeField(null=False)