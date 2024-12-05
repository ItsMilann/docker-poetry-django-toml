from django.urls import path
from django.urls.conf import include
from users.viewsets import ObtainTokenView

from .routers import router


urlpatterns = [
    path("api/v1/auth/token/", ObtainTokenView.as_view()),
    path("api/v1/", include(router.urls)),
]
