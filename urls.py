from django.conf.urls.defaults import *
from pcstore.views import *
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
from django.contrib.auth.views import login, logout


urlpatterns = patterns('',
    # Example:
    (r'^$', index),
    (r'^contacts/$', contacts),
    (r'^howto/$', howto),
    (r'^about/$', about),
    (r'^products/(\d+)/$', products),
    (r'^product_info/(\d+)/$', product_info),
    (r'^registration/$', register),
    (r'^login/$', login_view),
    (r'^logout/$', logout_view),
    (r'^remove/(\d+)/$', remove),
    (r'^show_cart/$', show_cart),
    (r'^order/$', order),
    (r'^my_orders/$', my_orders),
    (r'^site_media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),


    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)
