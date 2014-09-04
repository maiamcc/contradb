from django.conf.urls import patterns, url

from contratest import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^search$', views.search, name='search'),
    url(r'^results$', views.results, name='results'),
    url(r'^testsearch$', views.testsearch, name='testsearch'),
    url(r'^testresults$', views.testresults, name='testresults'),
)