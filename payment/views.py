from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader

from .models import Company, Department

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
    return render(request, 'payment/detail.html', context)

def results(request, company_id):
    response = "You're looking at the result of company %s."
    return HttpResponse(response % company_id)

def vote(request, company_id):
    return HttpResponse("You're voting on company %s." % company_id)
