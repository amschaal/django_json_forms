from django.shortcuts import render
from django.template.context import RequestContext
from forms import JSONForm
from models import JSONFormModel, Response as JSONFormResponse
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
                message = json_form.errors
        else:
            json_form = JSONForm(fields=fields)
    
    return render(request, 'json_form/test.html', {'json_form':json_form,'fields':fields,'message':message},context_instance=RequestContext(request))

def designer(request):
#     forms = JSONFormModel.objects.all()
    return render(request, 'json_form/designer.html', {},context_instance=RequestContext(request))

def forms(request):
    forms = JSONFormModel.objects.all()
    return render(request, 'json_form/list.html', {'forms':forms},context_instance=RequestContext(request))

def responses(request,pk):
    responses = JSONFormResponse.objects.filter(form_id=pk)
    return render(request, 'json_form/responses.html', {'responses':responses},context_instance=RequestContext(request))

def response(request,pk):
    response = JSONFormResponse.objects.get(pk=pk)
    return render(request, 'json_form/response.html', {'response':response},context_instance=RequestContext(request))

def form(request,pk):
    json_form = JSONFormModel.objects.get(pk=pk)
    message = ''
    if request.method == 'POST':
        form = json_form.get_form(request.POST,request.FILES)
        if form.is_valid():
            response = JSONFormResponse.objects.create(form=json_form,fields=json_form.fields,data=form.cleaned_data_with_files)
            print 'get data'
            print form.cleaned_data_with_files
            message = response.data
        else:
            message = form.errors
    else:
        form = json_form.get_form()
    
    return render(request, 'json_form/form.html', {'form':form,'message':message},context_instance=RequestContext(request))