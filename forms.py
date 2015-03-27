from django import forms
import json

class JSONForm(forms.Form):
    def __init__(self,*args,**kwargs):
        fields = json.loads(kwargs.pop('fields','[]'))
        super(JSONForm, self).__init__(*args, **kwargs)
        fh = FieldHandler(fields)
        self.fields = fh.formfields
        print self.fields
        
class FieldHandler():
    formfields = {}
    def __init__(self, fields):
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
#         options['max_length'] = int(field.get("max_length", "20") )
        return forms.FileField()
        return forms.CharField(**options)
    
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