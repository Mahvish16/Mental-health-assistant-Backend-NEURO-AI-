from django.contrib import admin
from .models import Questions,Disorder, DisorderSave

# Register your models here.
admin.site.register(Questions)
admin.site.register(Disorder)
admin.site.register(DisorderSave)



