from rest_framework.routers import DefaultRouter

from auth_app.views import AuthViewSet

router = DefaultRouter()
router.register("", AuthViewSet, basename="auth")

urlpatterns = router.urls
