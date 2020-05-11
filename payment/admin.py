from django.contrib import admin

from payment.models import *

admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Currency)
admin.site.register(Bills_Header)
admin.site.register(Bills_Detail)
