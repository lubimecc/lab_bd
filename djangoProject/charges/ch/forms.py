from django import forms
from .models import *


class FlatForm(forms.Form):
    flats = Charges.objects.values_list('flat_id').distinct()
    flat_list = []
    i = 1
    flat_list.append([0, 'Квартира'])
    for flat in flats:
        flat_list.append([i, flat[0]])
        i += 1

    flat_tuple = tuple(tuple(x) for x in flat_list)
    flats_form = forms.TypedChoiceField(label="Выберите квартиру",
                                        empty_value=2,
                                        coerce=int,
                                        choices=flat_tuple)


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charges
        fields = ('charge_amount', 'flat', 'datetime')
        labels = {'charge_amount': 'Сумма начисления',
                  'flat': 'Квартира',
                  'datetime': 'Дата'}

    def __init__(self, *args, **kwargs):
        super(ChargeForm, self).__init__(*args, **kwargs)
        self.fields['flat'].attrs={
            'id': 'id_charge_flat'
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payments
        fields = ('payment_amount', 'flat', 'datetime')
        labels = {'payment_amount': 'Сумма платежа',
                  'flat': 'Квартира',
                  'datetime': 'Дата'}
