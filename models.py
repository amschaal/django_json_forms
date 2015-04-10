from django.db import models
from django.core.urlresolvers import reverse
# from django import forms
from jsonfield import JSONField
from django.utils.html import format_html
import os


class JSONFormModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fields = JSONField(null=True, blank=True)
    def __unicode__(self):
        return self.name
    def get_form(self,*args):
        from forms import JSONModelForm
        print self.fields
        return JSONModelForm(*args,fields=self.fields)
    
class Response(models.Model):
    form = models.ForeignKey(JSONFormModel,related_name='responses')
    fields = JSONField(null=False,blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    data = JSONField(null=False,blank=False)
    def __init__(self,*args,**kwargs):
        super(Response,self).__init__(*args,**kwargs)
        self.field_hash={}
        for field in self.fields:
            self.field_hash[field['name']]=field
        for field in self.fields:
            field['label'] = self.get_label(field)
            field['value'] = self.get_value(field)
            if self.id:
                field['pretty_value'] = self.get_pretty_value(field)
#     def field_iterator(self):
#         fields = self.fields.copy()
#         for field in fields:
#             field['label'] = self.get_label(field)
#             field['value'] = self.get_value(field)
#             field['pretty_value'] = self.get_pretty_value(field)
#         return fields
#     def get_label_values(self):
#         return {self.get_label(field['name']): self.get_value(field['name']) for field in self.fields}
    def get_form(self):
        from forms import JSONModelForm
        return JSONModelForm(self.data,fields=self.fields)
    def get_label(self,field):
        return field.get('label',field['name'])
    def get_pretty_value(self,field):
        value = self.get_value(field)
        if field.get('type') in ['file']:
            try:
                value = os.path.basename(value)
            except:
                return value
            return format_html('<a href="%s">%s</a>' % (reverse('download_response_file',kwargs={'pk':self.id})+'?field='+field['name'],value))
        return value
    def get_value(self,field):
        return self.data[field['name']]
            
