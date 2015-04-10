from django.contrib import admin
from django.core.urlresolvers import reverse
from models import JSONFormModel
from forms import JSONFormModel_Form
from django.utils.html import format_html

def form_actions(obj):
    return format_html('<a href="%s">%s</a>, <a href="%s">%s</a>, <a href="%s">%s</a>' % (reverse('form_designer',kwargs={"pk":obj.id}),'Designer',reverse('responses',kwargs={"pk":obj.id}),'Responses',reverse('form',kwargs={"pk":obj.id}),'Form'))
form_actions.short_description = 'Actions'

class JSONFormModelAdmin(admin.ModelAdmin):
    model = JSONFormModel
    form = JSONFormModel_Form
    list_display = ('name','description',form_actions)
admin.site.register(JSONFormModel, JSONFormModelAdmin)
