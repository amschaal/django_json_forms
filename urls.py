from django.conf.urls import url
from django_json_forms import views


urlpatterns = [
    url(r'^designer/$', views.designer, name='designer'),
    url(r'^test/$', views.test, name='test_json_form'),
    url(r'^$', views.forms, name='forms'),
    url(r'^forms/(?P<pk>\d+)/$', views.form, name='form'),
    url(r'^forms/(?P<pk>\d+)/update_fields/$', views.update_form_fields, name='update_form_fields'),
    url(r'^forms/(?P<pk>\d+)/designer/$', views.form_designer, name='form_designer'),
    url(r'^forms/(?P<pk>\d+)/responses/$', views.responses, name='responses'),
    url(r'^responses/(?P<pk>\d+)/view/$', views.response, name='response'),
    url(r'^responses/(?P<pk>\d+)/download/$', views.download_response_file, name='download_response_file'),
]
