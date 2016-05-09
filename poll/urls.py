from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.display, name='displayurl'),
    url(r'^dummy/$', views.dummy, name='dummyurl'),
    url(r'^thanks/$', views.thanks, name='thanksurl'),
    url(r'^results/$', views.results, name='resultsurl'),
]
