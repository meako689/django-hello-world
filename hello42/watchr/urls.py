from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'watchr.views.request_list', name='request_list'),
)

