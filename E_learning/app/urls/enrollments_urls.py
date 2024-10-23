from django.urls import path, include
from rest_framework import routers
from E_learning.app import views

router = routers.DefaultRouter()
router.register(r'enrollments', views.EnrollmentsViewSet)

urlpatterns = router.urls
