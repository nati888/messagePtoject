from django.urls import path
from rest_framework.routers import DefaultRouter

from message.views import MessageViewSet, UserViewSet, LoginViewSet, LogoutViewSet

router = DefaultRouter()

router.register("messages", MessageViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path("accounts/login/", LoginViewSet.as_view()),
    path("accounts/logout/", LogoutViewSet.as_view())
]

urlpatterns += router.urls
