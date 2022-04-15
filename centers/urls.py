from rest_framework import routers

from .views import CertificationCenterView
router = routers.DefaultRouter()
router.register('', CertificationCenterView, 'certificationcenters')

urlpatterns = router.urls
