from django.contrib import admin

# Register your models here.

from .models import CertificationSession, RegisterInSession

admin.site.register(CertificationSession)
admin.site.register(RegisterInSession)
