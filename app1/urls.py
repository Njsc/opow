from django.conf.urls import url

from app1.views import add, detail, index, about, contact, do_register, do_login, do_logout, list

urlpatterns = [
    url(r'^add/$', add, name='add'),
    url(r'^list/$', list, name='list'),
    url(r'^detail/$', detail, name='detail'),
    url(r'^$', index, name='index'),
    url(r'^about/$', about, name='about'),
    url(r'^contact/$', contact, name='contact'),
    url(r'^register/$', do_register, name='register'),
    url(r'^login/$', do_login, name='login'),
    url(r'^logout/$', do_logout, name='logout'),
]
