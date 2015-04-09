from django.conf.urls import patterns, include, url

urlpatterns = patterns('',)


urlpatterns = patterns('',
    url(r'^designer/$', 'django_json_form.views.designer', name='designer'),
    url(r'^test/$', 'django_json_form.views.test', name='test_json_form'),
    url(r'^$', 'django_json_form.views.forms', name='forms'),
    url(r'^forms/(?P<pk>\d+)/$', 'django_json_form.views.form', name='form'),
    url(r'^forms/(?P<pk>\d+)/update_fields/$', 'django_json_form.views.update_form_fields', name='update_form_fields'),
    url(r'^forms/(?P<pk>\d+)/designer/$', 'django_json_form.views.form_designer', name='form_designer'),
    url(r'^forms/(?P<pk>\d+)/responses/$', 'django_json_form.views.responses', name='responses'),
    url(r'^responses/(?P<pk>\d+)/view/$', 'django_json_form.views.response', name='response'),
    url(r'^responses/(?P<pk>\d+)/download/$', 'django_json_form.views.download_response_file', name='download_response_file'),
    
)

