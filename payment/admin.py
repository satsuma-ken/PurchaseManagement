from django.contrib import admin

from payment.models import *

admin.site.register(Companies)
admin.site.register(Departments)
admin.site.register(Currencies)
admin.site.register(Bills_Header)
admin.site.register(Bills_Detail)
