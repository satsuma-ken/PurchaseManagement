from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template import loader
from decimal import Decimal, ROUND_HALF_UP

from .models import Company, Department, Bills_Header, Bills_Detail

def index(request):
    company_list = Company.objects.order_by('-create_datetime')[:5]
    context = {
        'company_list': company_list,
    }
    return render(request, 'payment/index.html', context)

def detail(request, company_id):
    company = get_object_or_404(Company, company_id=company_id)
    context = {
        'company': company,
    }
    print('detail')
    return render(request, 'payment/detail.html', context)

def results(request, company_id):
    response = "You're looking at the result of company %s."
    return HttpResponse(response % company_id)

def vote(request, company_id):
    return HttpResponse("You're voting on company %s." % company_id)

def bills(request):
    department_list = get_list_or_404(Department)
    context = {
        'department_list': department_list,
    }
    return render(request, 'payment/bills.html', context)

def bills_detail(request, invoice_id):
    bills_header = get_object_or_404(Bills_Header, invoice_id=invoice_id)
    bills_details = get_list_or_404(Bills_Detail, invoice_id=invoice_id)
    sumproduct = Decimal("0")
    for bill in bills_details:
        sumproduct += bill.product
    tax = sumproduct * Decimal("0.1")
    tax_adopt = sumproduct * Decimal("1.1")
    d_sumproduct = ""
    d_tax = ""
    d_tax_adopt = ""
    if float(sumproduct).is_integer:
        d_sumproduct = str(Decimal(sumproduct).quantize(Decimal("0"), ROUND_HALF_UP))
    else:
        d_sumproduct = str(float(sumproduct))

    if float(tax).is_integer:
        d_tax = str(Decimal(tax).quantize(Decimal("0"), ROUND_HALF_UP))
    else:
        d_tax = str(float(tax))
    
    if float(tax_adopt).is_integer:
        d_tax_adopt = str(Decimal(tax_adopt).quantize(Decimal("0"), ROUND_HALF_UP))
    else:
        d_tax_adopt = str(float(tax_adopt))
    context = {
        'bills_header': bills_header,
        'bills_details': bills_details,
        'sumproduct': d_sumproduct,
        'tax': d_tax,
        'tax_adopt': d_tax_adopt,
    }
    return render(request, 'payment/bills_detail.html', context)
