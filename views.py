from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.template.context import RequestContext
from django.http import HttpResponse, HttpResponseForbidden
from forms import JSONForm
from models import JSONFormModel, Response as JSONFormResponse
import json
from django.contrib.auth.decorators import user_passes_test
from decorators import download_permission, form_permission

def test(request):
    json_form = None
    fields = request.POST.get('fields',None)
    submitted = request.POST.get('submitted',None)
    message = None
    if fields:
        if submitted:
            json_form = JSONForm(request.POST,request.FILES,fields=fields)
            if json_form.is_valid():
                message = 'Form is valid'
            else:
                message = 'Validation Error'
        else:
            json_form = JSONForm(fields=fields)
    
    return render(request, 'json_form/test.html', {'json_form':json_form,'fields':fields,'message':message},context_instance=RequestContext(request))

def designer(request):
#     forms = JSONFormModel.objects.all()
    return render(request, 'json_form/designer.html', {},context_instance=RequestContext(request))

@form_permission()
def form_designer(request,pk):
    json_form = JSONFormModel.objects.get(pk=pk)
    print json_form.fields
    init = {'fields':json_form.fields,'id':json_form.id,'urls':{'update':reverse('update_form_fields',kwargs={"pk":pk})}}
    return render(request, 'json_form/designer.html', {'init':json.dumps(init),'json_form':json_form},context_instance=RequestContext(request))

def forms(request):
    forms = JSONFormModel.objects.all()
    return render(request, 'json_form/list.html', {'forms':forms},context_instance=RequestContext(request))

@form_permission()
def responses(request,pk):
    json_form = JSONFormModel.objects.get(pk=pk)
    return render(request, 'json_form/responses.html', {'responses':json_form.responses.all(),'json_form':json_form},context_instance=RequestContext(request))

def response(request,pk):
    response = JSONFormResponse.objects.get(pk=pk)
    return render(request, 'json_form/response.html', {'response':response},context_instance=RequestContext(request))

@form_permission()
def form(request,pk):
    json_form = JSONFormModel.objects.get(pk=pk)
    message = ''
    if request.method == 'POST':
        form = json_form.get_form(request.POST,request.FILES)
        if form.is_valid():
            response = form.create_response()#JSONFormResponse.objects.create(form=json_form,data=form.cleaned_data_with_files)
            print form.cleaned_data_with_files
            message = response.data
            return redirect('response',pk=response.id)
        else:
            message = 'Validation error'
    else:
        form = json_form.get_form()
    return render(request, 'json_form/form.html', {'message':message,'form':form,'json_form':json_form},context_instance=RequestContext(request))

@form_permission()
def update_form_fields(request,pk):
    json_form = JSONFormModel.objects.get(pk=pk)
    data = json.loads(request.body)
    json_form.fields = data['fields']
    json_form.save()
    return HttpResponse(json.dumps({'status':'success'}), content_type='application/json')

@download_permission()
def download_response_file(request,pk):
    from sendfile import sendfile
    field_name = request.GET.get('field')
    response = JSONFormResponse.objects.get(pk=pk)
    field = response.field_hash[field_name]
    if field.get('type') not in ['file']:
        return HttpResponseForbidden('Not a valid file field')
    path = response.data[field_name]
    return sendfile(request, path)
