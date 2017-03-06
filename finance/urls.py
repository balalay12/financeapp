from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(), name='index'),
    url(r'^login/$', views.UserLogin.as_view(), name='login'),
    url(r'^registration/$', views.UserRegistration.as_view(), name='registration'),
    url(r'^logout/$', views.UserLogout.as_view(), name='logout'),
    url(r'^accounts/add/$', views.AccountsCreate.as_view(), name='new_account'),
    url(r'^account/update/(?P<pk>[0-9]+)/$', views.AccountUpdate.as_view(), name='update_account'),
    url(r'^account/delete/(?P<pk>[0-9]+)/$', views.AccountDelete.as_view(), name='delete_account')
]