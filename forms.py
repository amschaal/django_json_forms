from django import forms
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
# from django.conf import settings
import json
from django_json_form.models import JSONFormModel
from django.core.urlresolvers import reverse
from django.utils.html import format_html

# class JSONFileField(forms.FileField):
# 
#     def clean(self, *args, **kwargs):
#         super(JSONFileField, self).clean(*args, **kwargs)
#         tmp_file = args[0]
# 
# #         if tmp_file.size > 6600000:
# #             raise forms.ValidationError("File is too large.")
# 
#         file_path = getattr(settings,'FILE_UPLOAD_TEMP_DIR')+'/'+tmp_file.name
# 
#         destination = open(file_path, 'wb+')
#         for chunk in tmp_file.chunks():
#             destination.write(chunk)
#         destination.close()
# 
#         try:
#             audio = MP3(file_path)
#             if audio.info.length > 300:
#                 os.remove(file_path)
#                 raise forms.ValidationError("MP3 is too long.")
# 
#         except (HeaderNotFoundError, InvalidMPEGHeader):
#             os.remove(file_path)
#             raise forms.ValidationError("File is not valid MP3 CBR/VBR format.")
#         os.remove(file_path)
#         return args

class JSONModelForm(forms.Form):
    def __init__(self,*args,**kwargs):
        fields = kwargs.pop('fields','[]')
        super(JSONModelForm, self).__init__(*args, **kwargs)
        fh = FieldHandler(fields)
        self.fields = fh.formfields
    def clean(self):
        super(JSONModelForm,self).clean()
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

class JSONForm(forms.Form):
    def __init__(self,*args,**kwargs):
        fields = json.loads(kwargs.pop('fields','[]'))
        super(JSONForm, self).__init__(*args, **kwargs)
        fh = FieldHandler(fields)
        self.fields = fh.formfields
        
class JSONFormModel_Form(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(JSONFormModel_Form, self).__init__(*args, **kwargs)
        if self.instance:
            self.fields['fields'].help_text = format_html('<h3>Use <a href="%s">Designer</a></h3>'%reverse('form_designer',kwargs={"pk":self.instance.id}))
    class Meta:
        model=JSONFormModel
        fields = ('name','description','fields')

class FieldHandler():
    def __init__(self, fields):
        self.formfields = {}
        for field in fields:
            options = self.get_options(field)
            f = getattr(self, "create_field_for_"+field['type'] )(field, options)
            self.formfields[field['name']] = f

    def get_options(self, field):
        options = {}
        options['label'] = field['label']
        options['help_text'] = field.get("help_text", None)
        options['required'] = bool(field.get("required", 0) )
        return options

    def create_field_for_text(self, field, options):
        options['max_length'] = int(field.get("max_length", "20") )
        return forms.CharField(**options)
    
    def create_field_for_file(self, field, options):
        return forms.FileField(**options)
    
    def create_field_for_textarea(self, field, options):
        options['max_length'] = int(field.get("max_value", "9999") )
        return forms.CharField(widget=forms.Textarea, **options)

    def create_field_for_integer(self, field, options):
        options['max_value'] = int(field.get("max_value", "999999999") )
        options['min_value'] = int(field.get("min_value", "-999999999") )
        return forms.IntegerField(**options)

    def create_field_for_radio(self, field, options):
        options['choices'] = [ (c['value'], c['name'] ) for c in field['choices'] ]
        return forms.ChoiceField(widget=forms.RadioSelect,   **options)

    def create_field_for_select(self, field, options):
        options['choices']  = [ (c['value'], c['name'] ) for c in field['choices'] ]
        return forms.ChoiceField(  **options)

    def create_field_for_checkbox(self, field, options):
        return forms.BooleanField(widget=forms.CheckboxInput, **options)
    
def get_form(jstr):
    fields=json.loads(jstr)
    fh = FieldHandler(fields)
    return type('DynaForm', (forms.Form,), fh.formfields )