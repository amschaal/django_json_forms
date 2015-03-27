from django.conf.urls import patterns, include, url

urlpatterns = patterns('',)


urlpatterns = patterns('',
    url(r'^test/$', 'django_json_form.views.test', name='test_json_form'),
    url(r'^list/$', 'django_json_form.views.forms', name='forms'),
    url(r'^forms/(?P<pk>\d+)/$', 'django_json_form.views.form', name='form'),
    
)

