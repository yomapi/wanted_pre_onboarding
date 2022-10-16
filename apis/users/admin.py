from django.contrib import admin
from users.models import Applicant, Company


admin.site.register(Applicant)
admin.site.register(Company)
