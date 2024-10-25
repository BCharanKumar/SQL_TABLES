from django.contrib import admin

# Register your models here.
from cherry.models import *

admin.site.register(Dept)
admin.site.register(Emp)
admin.site.register(Salgrade)
