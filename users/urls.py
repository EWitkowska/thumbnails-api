from rest_framework.routers import DefaultRouter

from .views import UserViewSet, AccountViewSet

router = DefaultRouter()

router.register("users", UserViewSet, basename="users")
router.register("accounts", AccountViewSet, basename="accounts")

app_name = "users"
urlpatterns = router.urls
