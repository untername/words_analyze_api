from rest_framework.routers import DefaultRouter
from .views import HomeView


router = DefaultRouter()
router.register(r'', HomeView)

urlpatterns = router.urls
