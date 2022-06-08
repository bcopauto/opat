from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from .views import oplogin, apps, home, oplogout
from logana.views import rp_err, upload, project_dash, create, processing_details, erp_details, googlebot_details

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('login/', oplogin, name='login'),
    path('logout/', oplogout, name='logout'),
    path('apps/', apps),
    path('logana/erp', rp_err), 
    path('logana/upload', upload),
    path('logana/projects', project_dash),
    path('logana/create', create, name='create'),
    path('logana/processing-details', processing_details, name='prdetails'),
    path('logana/erp', erp_details, name='erp'),
    path('logana/googlebot', googlebot_details, name='googlebot')

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
