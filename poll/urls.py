from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.display, name='displayurl'),
    url(r'^dummy/$', views.dummy, name='dummyurl'),
    url(r'^thanks/$', views.thanks, name='thanksurl'),
    url(r'^results/$', views.results, name='resultsurl'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^org_entering/$', views.user_orgName_form, name='user_orgName_formURL'),
    url(r'^org_dummy/$', views.user_orgName, name='user_orgNameURL')
]
