from django.contrib import admin

from .models import VcCL, VcMV, VcDNS

admin.site.register(VcCL)
admin.site.register(VcDNS)
admin.site.register(VcMV)
