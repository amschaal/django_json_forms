from django.conf.urls import patterns, include, url

urlpatterns = patterns('',)


urlpatterns = patterns('',
    url(r'^designer/$', 'django_json_form.views.designer', name='designer'),
    url(r'^test/$', 'django_json_form.views.test', name='test_json_form'),
    url(r'^list/$', 'django_json_form.views.forms', name='forms'),
    url(r'^forms/(?P<pk>\d+)/$', 'django_json_form.views.form', name='form'),
    url(r'^forms/(?P<pk>\d+)/responses/$', 'django_json_form.views.responses', name='responses'),
    url(r'^responses/(?P<pk>\d+)/view/$', 'django_json_form.views.response', name='response'),
    
)

