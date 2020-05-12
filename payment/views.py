from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template import loader

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
    sumproduct = 0
    for bill in bills_details:
        sumproduct += bill.product
    tax = sumproduct * 0.1
    tax_adopt = sumproduct * 1.1
    context = {
        'bills_header': bills_header,
        'bills_details': bills_details,
        'sumproduct': sumproduct,
        'tax': tax,
        'tax_adopt': tax_adopt,
    }
    return render(request, 'payment/bills_detail.html', context)
