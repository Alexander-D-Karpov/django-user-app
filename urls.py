from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .api import AuthViewSet, ListUsersViewSet, GetUserView
from .views import *

urlpatterns = [
    path("login/", login, name="login"),
    path("logout/", logout, name="logout"),
    path("register/", register, name="register"),
    path("settings/", settings, name="settings"),
    path("settings/tg_unlick", tg_unlink, name="tg_unlick"),
    path("", user_list, name="users"),
    path("profile/<str:username>/", profile, name="profile"),
    path("api/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("api/list", ListUsersViewSet.as_view(), name="user_list"),
    path("api/list/<int:id>", GetUserView.as_view({"get": "list"}), name="user_api_id"),
]

router = routers.DefaultRouter(trailing_slash=False)
router.register("api", AuthViewSet, basename="api_auth")

urlpatterns += router.urls
