from ..urls.users_urls import urlpatterns as users_urls
from ..urls.enrollments_urls import urlpatterns as enrollments_urls
from ..urls.courses_urls import urlpatterns as courses_urls
from ..urls.auth_urls import urlpatterns as auth_urls
urlpatterns = users_urls + enrollments_urls + courses_urls + auth_urls

