"""wpk URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from machina import urls as machina_urls
from . import views




urlpatterns = [
    path('admin/', admin.site.urls),
    path('wpk/', include(machina_urls)),
    path('chat/', views.chat),
    path('accounts/', include('django.contrib.auth.urls')),
    path('logout/', views.logout_view),
    path('poufne/', views.poufne),
    path('dzienks/', views.dzienks),
    path('w/', views.wiadomosci),
    path('sp/', views.skrzynka_pacjenta),
    path('poufneajaxp/', views.poufneajaxp),
    path('poufneajax/', views.poufneajax),
    path('usunwiadomosc/', views.usunwiadomosc),
    path('usunwiadomoscf/', views.usunwiadomoscf),
    path('statusskype/', views.statusskype),
    path('skypeframe/', views.skypeframe),
    path('newsy/', views.newsy),
    path('', views.hi),
    path('.well-known/pki-validation/F965227573D05E85617E32BD3E1E9625.txt', views.ssl),
    path('messages/', include('django_messages.urls')),
    path('liczbaodebranychpw/', views.liczbaodebranychpw)

    ]



##
#if settings.DEBUG:
#    urlpatterns += patterns('',
#        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.MEDIA_ROOT,
#        }),
#        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
#            'document_root': settings.STATIC_ROOT,
#        }),
#)