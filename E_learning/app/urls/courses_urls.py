from .. import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'courses', views.CoursesViewSet)

urlpatterns = router.urls
