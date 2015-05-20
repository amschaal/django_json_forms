from django.db.models.signals import pre_delete, post_delete, post_save, pre_save
from models import Response
from django.dispatch import receiver
import os
#@todo: add signal to reset group permissions post_save

@receiver(pre_delete,sender=Response)
def delete_response(sender,**kwargs):
    instance = kwargs['instance']
    directories = []
    for field in instance.fields:
        if field.get('type') == 'file':
            try:
                if os.path.isfile(instance.data[field['name']]):
                    os.remove(instance.data[field['name']])
                    directory = os.path.dirname(instance.data[field['name']])
                    if directory not in directories:
                        directories.append(directory)
            except:
                pass
    for directory in directories:
        try:
            os.rmdir(directory)
        except:
            print 'Could not delete directory %s, it may not be empty.' % directory
