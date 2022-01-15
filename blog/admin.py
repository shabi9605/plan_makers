from django.contrib import admin
from . models import * 
from django.contrib.admin.decorators import register

# Register your models here.
admin.site.register(Register)
admin.site.register(Complaints)
admin.site.register(Feedback)
admin.site.register(Requiremt)
admin.site.register(Chat)

class LeaveAdmin(admin.ModelAdmin):
    list_display=('user','startdate','days','reason','status','date')

admin.site.register(Leave,LeaveAdmin)
admin.site.register(PriceTable)