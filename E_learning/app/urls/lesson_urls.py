from django.urls import path, include
from rest_framework import routers
from E_learning.app import views
from E_learning.app.views.lesson_views import LessonViewSet

router = routers.DefaultRouter()
router.register('lesson', LessonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
