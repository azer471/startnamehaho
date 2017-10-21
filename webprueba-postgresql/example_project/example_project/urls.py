from __future__ import unicode_literals
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url('',include("posts.urls")),
    url(r'^comments/', include("comments.urls", namespace='comments')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
