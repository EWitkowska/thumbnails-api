from rest_framework.routers import DefaultRouter

from .views import ImageViewSet, ExpiringLinkViewSet

router = DefaultRouter()

router.register("images", ImageViewSet)
router.register("expiring-links", ExpiringLinkViewSet, basename="expiring-link")


app_name = "thumbnails"
urlpatterns = router.urls
