"""msite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from pestyle.views import *
from django.contrib.auth.views import logout
from django.views.generic.base import RedirectView

urlpatterns = [
    url(r'^$', main_page, name='main_page'),
    url(r'^look_choice/$', look_choice, name='look_choice'),
    url(r'^login_window/$', RedirectView.as_view(url='/#login_window'), name='login'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^get_looks/$', get_looks, name='get_looks'),
    url(r'^like_look/$', like_look, name='like_look'),
    url(r'^get_items/$', get_items, name='get_items'),
    url(r'^item_window/$', item_window, name='item_window'),
]
