from django.urls import re_path, path
from chatgptcomments import views

urlpatterns = [
    re_path(r'^$', views.showIndex, name='index'),
    re_path(r'^analysis', views.showAnalysis, name='index'),
    re_path(r'^search', views.showSearch, name='search'),
    re_path(r'^qachat', views.showQAchat, name='qachat'),
    re_path(r'^help', views.showHelp, name='help'),
    re_path(r'^keysearch', views.searchindex, name='searchIndex'),
    re_path(r'^getAnswering', views.getAnswering, name='getAnswer'),
]
