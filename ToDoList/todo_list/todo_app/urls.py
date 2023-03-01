from rest_framework.routers import DefaultRouter

from todo_app.views import TodoViewSet

router = DefaultRouter()
router.register("", TodoViewSet, basename="")

urlpatterns = router.urls
