#from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('certificationcenters/', include('centers.urls'), name='certificationcenters'),
                  path('sessions/', include('certifsessions.urls')),
                  #path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  path('users/', include('users.urls'), name='users'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

