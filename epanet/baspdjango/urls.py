from django.conf.urls import url
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^api/', include('basp.urls')),

]

#static(r'docs/', document_root=settings.DOCS_ROOT,path='index.html')

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)