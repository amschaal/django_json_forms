from django import forms
from django.core.files.uploadedfile import TemporaryUploadedFile, InMemoryUploadedFile
# from django.conf import settings
import json, os
from datetime import datetime
from django_json_forms.models import JSONFormModel
from django.utils.html import format_html
from django.conf import settings
from django_json_forms.models import Response
from crispy_forms.layout import HTML, Fieldset, Layout
from crispy_forms.helper import FormHelper
from django.urls.base import reverse
UPLOAD_DIRECTORY = getattr(settings,'DJANGO_JSON_FORMS_UPLOAD_DIRECTORY')
GET_UPLOAD_PATH = getattr(settings,'DJANGO_JSON_FORMS_GET_UPLOAD_PATH',False)
from django.utils.module_loading import import_string


class JSONModelForm(forms.Form):
    def __init__(self,*args,**kwargs):
        self.json_form_model = kwargs.pop('JSONFormModel')
        super(JSONModelForm, self).__init__(*args, **kwargs)
        fh = FieldHandler(self.json_form_model.fields)
        self.fields = fh.formfields
        lh = LayoutHandler(self.json_form_model.fields)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = lh.layout
    def create_response(self):
        if self.is_valid():
            if not hasattr(self, 'response'):
                self.response = Response.objects.create(form=self.json_form_model,data={})
                self.cleaned_data_with_files = self.cleaned_data.copy()
                file_directory = os.path.join(UPLOAD_DIRECTORY,str(datetime.now().year),'%02d' % datetime.now().month,'%02d' % datetime.now().day, 'response_%d'%self.response.id)
                os.makedirs(file_directory)
                for key, value in self.cleaned_data.items():
                    if isinstance(value,(TemporaryUploadedFile,InMemoryUploadedFile)):
                        file_path = os.path.join(file_directory,value.name)
#                         if GET_UPLOAD_PATH:
#                             get_upload_path = import_string(GET_UPLOAD_PATH)
#                             file_path = get_upload_path(self,key,value)
                        destination = open(file_path, 'wb+')
                        for chunk in value.chunks():
                            destination.write(chunk)
                        destination.close()
                        self.cleaned_data_with_files[key]= file_path
                self.response.data = self.cleaned_data_with_files
                self.response.save()
                print(self.response.data)
            return self.response

class JSONForm(forms.Form):
    def __init__(self,*args,**kwargs):
#         print kwargs
#         try:
#             fields = json.loads(kwargs.pop('fields','[]'))
#         except:
        fields = kwargs.pop('fields','[]')
        if not isinstance(fields,list):
            raise Exception('fields argument must be a list')
        super(JSONForm, self).__init__(*args, **kwargs)
        fh = FieldHandler(fields)
        self.fields = fh.formfields
        lh = LayoutHandler(fields)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = lh.layout
        
class JSONFormModel_Form(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        super(JSONFormModel_Form, self).__init__(*args, **kwargs)
        if self.instance:
            if self.instance.id:
                self.fields['fields'].help_text = format_html('<h3>Use <a href="%s">Designer</a></h3>'%reverse('form_designer',kwargs={"pk":self.instance.id}))
    class Meta:
        model=JSONFormModel
        fields = ('name','description','fields')


class LayoutHandler():
    def __init__(self, fields):
        self.layout_items = []
#         print fields
        for field in fields:
            if 'type' in field:
#                 print(field['type'])
                if field['type'] == 'layout_html':
                    self.layout_items.append(HTML(field['html']))
                else:
                    self.layout_items.append(field['name'])
        self.layout = Layout(*self.layout_items)

class FieldHandler():
    def __init__(self, fields):
        self.formfields = {}
        for field in fields:
            if 'type' in field:
                if hasattr(self, "create_field_for_"+field['type']):
                    options = self.get_options(field)
                    f = getattr(self, "create_field_for_"+field['type'] )(field, options)
                    self.formfields[field['name']] = f
    def get_options(self, field):
        options = {}
        options['label'] = field['label']
        options['help_text'] = field.get("help_text", None)
        options['required'] = bool(field.get("required", 0) )
        return options
    @staticmethod
    def curate_choices(options):
        choices = []
        for c in options:
            if 'value' in c and not 'name' in c:
                choices.append((c['value'],c['value']))
            elif 'name' in c and not 'value' in c:
                choices.append((c['name'],c['name']))
            elif 'name' in c and 'value' in c:
                choices.append((c['value'],c['name']))
        return choices
    def create_field_for_text(self, field, options):
        options['max_length'] = int(field.get("max_length", "250") )
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
        options['choices'] = FieldHandler.curate_choices(field['choices'])
        return forms.ChoiceField(widget=forms.RadioSelect,   **options)

    def create_field_for_select(self, field, options):
        options['choices'] = FieldHandler.curate_choices(field['choices'])
        return forms.ChoiceField(  **options)

    def create_field_for_checkbox(self, field, options):
        return forms.BooleanField(widget=forms.CheckboxInput, **options)
    
    def create_field_for_multicheckbox(self, field, options):
        options['choices'] = FieldHandler.curate_choices(field['choices'])
        options['widget'] = forms.CheckboxSelectMultiple
        return forms.MultipleChoiceField(  **options)

def get_form(jstr):
    fields=json.loads(jstr)
    fh = FieldHandler(fields)
    return type('DynaForm', (forms.Form,), fh.formfields )