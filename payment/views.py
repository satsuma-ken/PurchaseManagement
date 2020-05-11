from django.http import HttpResponse
from django.template import loader

from .models import Company

def index(request):
    company_list = Company.objects.order_by('-create_datetime')[:5]
    template = loader.get_template('payment/index.html')
    context = {
        'company_list': company_list
    }
    return HttpResponse(template.render(context, request))

def detail(request, company_id):
    return HttpResponse("You're looking at company %s." % company_id)

def results(request, company_id):
    response = "You're looking at the result of company %s."
    return HttpResponse(response % company_id)

def vote(request, company_id):
    return HttpResponse("You're voting on company %s." % company_id)
