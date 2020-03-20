from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Donor, Hospital

# Register your models here.


admin.site.register(Donor)
admin.site.register(Hospital)