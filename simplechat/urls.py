from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()


urlpatterns = patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout', kwargs={'next_page': '/'}),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'simplechat.views.home', name='home'),
    url(r'^messages/', include('apps.messages.urls')),

    # Examples:
    # url(r'^$', 'simplechat.views.home', name='home'),
    # url(r'^simplechat/', include('simplechat.foo.urls')),

)
