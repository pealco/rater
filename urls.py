from django.conf.urls.defaults import patterns, include, url

#from django.contrib import admin
#admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'ratings.views.main', name='main'),
    url(r'^rate/(\d+)/(yes|no|notsure)/$', 'ratings.views.rate', name='rate'),
    url(r'^data\.png$', 'ratings.views.plot', name='plot'),

#    url(r'^admin/', include(admin.site.urls)),
)
