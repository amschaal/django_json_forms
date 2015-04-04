from django.db import models
# from django import forms
from jsonfield import JSONField


class JSONFormModel(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    fields = JSONField(null=False,blank=False)
    def __unicode__(self):
        return self.name
    def get_form(self,*args):
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
    def get_label_values(self):
        return {self.get_label(field['name']): self.get_value(field['name']) for field in self.fields}
    def get_form(self):
        return JSONModelForm(self.data,fields=self.fields)
    def get_label(self,name):
        field = self.field_hash[name]
        return field.get('label',name)
    def get_value(self,name):
        field = self.field_hash[name]
        return self.data[name]
