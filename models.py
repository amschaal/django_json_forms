from django.db import models
from django import forms
from jsonfield import JSONField
from forms import FieldHandler
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
class JSONForm(forms.Form):
    def __init__(self,*args,**kwargs):
        fields = kwargs.pop('fields','[]')
        super(JSONForm, self).__init__(*args, **kwargs)
        fh = FieldHandler(fields)
        self.fields = fh.formfields
    def clean(self):
        super(JSONForm,self).clean()
        if self.is_valid() and not hasattr(self, 'cleaned_data_with_files'):
            self.cleaned_data_with_files = self.cleaned_data.copy()
            for key, value in self.cleaned_data.iteritems():
                if isinstance(value,(TemporaryUploadedFile,InMemoryUploadedFile)):
                    print key
                    file_path = '/tmp'+'/'+value.name
                    destination = open(file_path, 'wb+')
                    for chunk in value.chunks():
                        destination.write(chunk)
                    destination.close()
                    self.cleaned_data_with_files[key]= file_path
            
    def get_data(self, commit=True):
        if not self.is_valid():
            return None
#         print self.cleaned_data
        self.cleaned_data_with_files = self.cleaned_data.copy()
        for key, value in self.cleaned_data.iteritems():
            if isinstance(value,(TemporaryUploadedFile,InMemoryUploadedFile)):
                print key
                file_path = '/tmp'+'/'+value.name
                destination = open(file_path, 'wb+')
                for chunk in value.chunks():
                    destination.write(chunk)
                destination.close()
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
    def __init__(self,*args,**kwargs):
        super(Response,self).__init__(*args,**kwargs)
        self.field_hash={}
        for field in self.fields:
            self.field_hash[field['name']]=field
    def get_label_values(self):
        return {self.get_label(field['name']): self.get_value(field['name']) for field in self.fields}
    def get_form(self):
        return JSONForm(self.data,fields=self.fields)
    def get_label(self,name):
        field = self.field_hash[name]
        return field.get('label',name)
    def get_value(self,name):
        field = self.field_hash[name]
        return self.data[name]
