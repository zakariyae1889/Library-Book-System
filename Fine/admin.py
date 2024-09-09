from django.contrib import admin

# Register your models here.
from .models import *
class FineAdmin(admin.ModelAdmin):
   list_display=("id","user",'borrow','amount',"paid")
   
admin.site.register(Fine,FineAdmin)
admin.site.register(Payment)