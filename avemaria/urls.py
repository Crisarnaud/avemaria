from django.urls import path
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static


from . import views

urlpatterns = [
    path("", views.index, name="index"),
    url(r'^book/(?P<id>[0-9]+)$', views.show_book),
    url(r'^login/$', views.login_view, name='login'),
    url(r'^pdf_viewer/$', views.pdf_viewer, name='pdf_viewer'),
    # url(r'^special/',views.special,name='special'),
    url(r'^register/$', views.register, name='register'),
    url(r'^user_profile/$', views.user_profile, name='user_profile'),
    url(r'^about/$', views.about, name='about'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^passwd_forgot/$', views.passwd_forgot, name='passwd_forgot'),

]
