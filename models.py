from django.db import models
from django import forms
from jsonfield import JSONField
from forms import FieldHandler

class JSONForm(forms.Form):
    def __init__(self,*args,**kwargs):
        fields = kwargs.pop('fields','[]')
        super(JSONForm, self).__init__(*args, **kwargs)
        fh = FieldHandler(fields)
        self.fields = fh.formfields

class JSONFormModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fields = JSONField(null=False,blank=False)
    def __unicode__(self):
        return self.name
    def get_form(self,*args):
        return JSONForm(*args,fields=self.fields)
    
class Response(models.Model):
    form = models.ForeignKey(JSONFormModel,related_name='responses')
    fields = JSONField(null=False,blank=False)
    timestamp = models.DateTimeField(auto_now=True)
    data = JSONField(null=False,blank=False)
    def get_form(self):
        return JSONForm(self.data,fields=self.fields)
    
