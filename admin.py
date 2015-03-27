from django.contrib import admin
from models import JSONFormModel

class JSONFormModelAdmin(admin.ModelAdmin):
    model = JSONFormModel
admin.site.register(JSONFormModel, JSONFormModelAdmin)
