from django.contrib import admin
from .models import *

# Register your models here.


class categoryslug(admin.ModelAdmin):
    prepopulated_fields = {"slug" : ("typeName",)}
admin.site.register(Cate, categoryslug)


class deviceslug(admin.ModelAdmin):
    prepopulated_fields = {"slugModel" : ("modelName",)}
admin.site.register(Device, deviceslug)

admin.site.register(DeviceFeatures)

admin.site.register(Image)


