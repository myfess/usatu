from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import index, health
from app.train import train_page, add_words, teachers_list

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index),
    url(r'^train$', train_page),
    url(r'^test$', add_words), 
    url(r'^teachers/?$', teachers_list),     
    url(r'^health$', health),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
