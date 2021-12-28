from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from .forms import FlatForm, ChargeForm, PaymentForm
from .models import *


# Create your views here.

def charges_def(charges, flats):
    charge_dict = {}
    for flat in flats:
        charge_dict[flat[0]] = []
        for i in range(1, 13):
            f = False
            for charge in charges:
                if charge.flat_id == flat[0] and charge.datetime.month == i and not f:
                    charge_dict[flat[0]].append(round(charge.charge_amount, 2))
                    f = True
            if not f:
                charge_dict[flat[0]].append('0.0')
    return charge_dict


def payments_def(payments, flats):
    payment_dict = {}
    for flat in flats:
        payment_dict[flat[0]] = []
        for i in range(1, 13):
            f = False
            for payment in payments:
                if payment.flat_id == flat[0] and payment.datetime.month == i and not f:
                    payment_dict[flat[0]].append(round(payment.payment, 2))
                    f = True
            if not f:
                payment_dict[flat[0]].append('0.0')
    return payment_dict


def saldo_def(saldo, flats):
    saldo_dict = {}
    print()
    print('saldo_def')
    print()
    print(len(flats))
    for flat in flats:
        temp = 0
        saldo_dict[flat[0]] = []
        for i in range(1, 13):
            f = False
            for sal in saldo:
                if sal.flat == flat[0] and sal.datetime.month == i and not f:
                    if temp == 0:
                        saldo_dict[flat[0]].append(round(sal.saldo_amount, 2))
                        temp += round(sal.saldo_amount, 2)
                    else:
                        saldo_dict[flat[0]].append(round((sal.saldo_amount + temp), 2))
                        temp += sal.saldo_amount
                    f = True
            if not f:
                saldo_dict[flat[0]].append('0.0')

    return saldo_dict


def selected_flat_charges(request, charges):
    selected_numbers_list = []
    selected_flat = request.GET.get('selected_flat')
    for i in range(1, 13):
        f = False
        if selected_flat:
            for charge in charges:
                if charge.flat_id == int(selected_flat) and charge.datetime.month == i and not f:
                    selected_numbers_list.append(round(charge.charge_amount, 2))
                    f = True
            if not f:
                selected_numbers_list.append('0.0')
    return selected_numbers_list


def selected_flat_payments(request, payments):
    selected_numbers_list = []
    selected_flat = request.GET.get('selected_flat')
    for i in range(1, 13):
        f = False
        if selected_flat:
            for payment in payments:
                if payment.flat_id == int(selected_flat) and payment.datetime.month == i and not f:
                    selected_numbers_list.append(round(payment.payment, 2))
                    f = True
            if not f:
                selected_numbers_list.append('0.0')
    return selected_numbers_list


def out_saldo(saldo_dict):
    out_saldo = {}
    out_saldo_dict = {}
    for key in saldo_dict:
        out_saldo[key] = []
        for value in saldo_dict[key]:
            if value != '0.0':
                out_saldo[key].append(value)
        out_saldo_dict[key] = out_saldo[key][len(out_saldo[key]) - 1]

    return out_saldo_dict


def date_difference(flats, saldo_dict):
    flat_diff = {}

    latest_payment = Payments.objects.raw('''   SELECT payment_id, flat_id, MONTH(datetime) as payment_month
                                                FROM ch_payments
                                                GROUP BY flat_id
                                                ORDER BY 2 DESC''')

    latest_charge = Charges.objects.raw('''SELECT charge_id, flat_id, charge_amount, MONTH(datetime) as charge_month
                                            FROM ch_charges
                                            GROUP BY flat_id
                                            ORDER BY 2 DESC''')

    saldo = out_saldo(saldo_dict)

    for flat in flats:
        j = 0
        for sal in saldo:
            if sal == flat[0] and saldo[sal] < 0:
                j = 1
        if j == 1:
            continue
        lat_flat_pay = 0
        lat_flat_charge = 0

        for val in latest_payment:
            if val.flat_id == flat[0]:
                lat_flat_pay = val.payment_month
        for val in latest_charge:
            if val.flat_id == flat[0]:
                lat_flat_charge = val.charge_month

        flat_diff[flat] = lat_flat_charge - lat_flat_pay

    return flat_diff


def latest_charge(charge_dict):
    latest_charge = {}
    latest_charge_dict = {}
    for key in charge_dict:
        latest_charge[key] = []
        for value in charge_dict[key]:
            if value != '0.00':
                latest_charge[key].append(value)
        latest_charge_dict[key] = latest_charge[key][len(latest_charge[key]) - 1]

    return latest_charge_dict


def home_page(request):
    charges = Charges.objects.all()
    payments = Payments.objects.raw(''' SELECT payment_id, SUM(payment_amount) as payment, flat_id, datetime
                                        FROM ch_payments 
                                        GROUP BY flat_id, MONTH(datetime), YEAR(datetime)''')
    saldo = Saldo.objects.all()
    flats = Saldo.objects.values_list('flat').distinct()

    charge_dict = charges_def(charges, flats)
    payment_dict = payments_def(payments, flats)
    saldo_dict = saldo_def(saldo, flats)

    out_saldo_dict = out_saldo(saldo_dict)
    latest_charge_dict = latest_charge(charge_dict)

    time_diff = date_difference(flats, saldo_dict)

    flat_form = FlatForm()
    charge_form = ChargeForm()
    payment_form = PaymentForm()
    input_table(request)
    data = {'flats': flats,
            'charge_dict': charge_dict,
            'payment_dict': payment_dict,
            'saldo_dict': saldo_dict,
            'flat_form': flat_form,
            'out_saldo_dict': out_saldo_dict,
            'latest_charge_dict': latest_charge_dict,
            'time_diff': time_diff,
            'charge_form': charge_form,
            'payment_form': payment_form
            }

    return render(request, 'charges/home.html', context=data)


def input_table(request):
    charges = Charges.objects.all()
    payments = Payments.objects.raw(''' SELECT payment_id, SUM(payment_amount) as payment, flat_id, datetime
                                                FROM ch_payments 
                                                GROUP BY flat_id, MONTH(datetime), YEAR(datetime)''')
    selected_flat_payments_list = selected_flat_payments(request, payments)
    selected_flat_charges_list = selected_flat_charges(request, charges)
    data = [selected_flat_charges_list, selected_flat_payments_list]
    return JsonResponse({'data': data})


def charge_input(request):
    if request.method == 'POST':
        amount = request.POST['charge_amount']
        flat = request.POST['charge_flat']
        date = request.POST['charge_date']

        datedate = datetime.strptime(date, '%Y-%m-%d %H:%M')

        Charges.objects.create(
            charge_amount=amount,
            flat_id=flat,
            datetime=date
        ).save()

        payment_sum = 0.00
        for payment in Payments.objects.filter(flat_id=flat,
                                               datetime__month=datedate.month,
                                               datetime__year=datedate.year):
            payment_sum += payment.payment_amount

        try:
            saldo_dict = Saldo.objects.get(datetime__month=datedate.month,
                                     datetime__year=datedate.year,
                                     flat=flat)
            saldo_dict.saldo_amount = amount - payment_sum
            saldo_dict.save()
        except Saldo.DoesNotExist:
            Saldo.objects.create(
                saldo_amount=float(amount),
                flat=flat,
                datetime=date
            ).save()


        return HttpResponse('')


def payment_input(request):
    if request.method == 'POST':
        amount = request.POST['payment_amount']
        flat = request.POST['payment_flat']
        date = request.POST['payment_date']
        datedate = datetime.strptime(date, '%Y-%m-%d %H:%M')

        Payments.objects.create(
            payment_amount=amount,
            flat_id=flat,
            datetime=date
        ).save()

        charge_dict = Charges.objects.filter(datetime__month=datedate.month,
                                        datetime__year=datedate.year,
                                        flat_id=flat)

        charge = 0.0
        for ch in charge_dict:
            charge += ch.charge_amount

        try:
            saldo_dict = Saldo.objects.get(datetime__month=datedate.month,
                                     datetime__year=datedate.year,
                                     flat=flat)
            saldo_dict.saldo_amount = charge - float(amount)
            saldo_dict.save()
        except Saldo.DoesNotExist:
            Saldo.objects.create(
                saldo_amount=float(amount) * (-1),
                flat=flat,
                datetime=date
            ).save()



    return HttpResponse('')
