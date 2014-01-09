from django.conf.urls import patterns, include, url
from views import UserEditView

urlpatterns = patterns('',
    url(r'^edit/(?P<pk>[\d+])/$',
        UserEditView.as_view(),
        name='user_edit'),
)

