from django.contrib.auth import login, logout
from django.core.exceptions import ImproperlyConfigured
from rest_framework import status, viewsets, generics, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from user import serializers
from user.models import Person
from user.services.change_password import change_password
from user.services.create_user import create_user
from user.services.get_and_authenticate_user import get_and_authenticate_user
from user.services.update_user_info import update_user_info


class AuthViewSet(viewsets.GenericViewSet):
    permission_classes = [
        AllowAny,
    ]
    serializer_class = serializers.EmptySerializer
    serializer_classes = {
        "login": serializers.UserLoginSerializer,
        "register": serializers.UserRegisterSerializer,
        "password_change": serializers.PasswordChangeSerializer,
        "update_user_info": serializers.AuthUserSerializer,
        "get_user_info": serializers.AuthUserSerializer,
    }

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_and_authenticate_user(**serializer.validated_data)
        data = serializers.AuthUserSerializer(user).data
        login(request, user)
        return Response(data=data, status=status.HTTP_200_OK)

    def get_serializer_class(self):
        if not isinstance(self.serializer_classes, dict):
            raise ImproperlyConfigured("serializer_classes should be a dict mapping.")

        if self.action in self.serializer_classes.keys():
            return self.serializer_classes[self.action]
        return super().get_serializer_class()

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = create_user(**serializer.data)
        data = serializers.AuthUserSerializer(user).data
        login(request, user)
        return Response(data=data, status=status.HTTP_201_CREATED)

    @action(
        methods=[
            "POST",
        ],
        detail=False,
    )
    def logout(self, request):
        logout(request)
        data = {"message": "Sucessfully logged out"}
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def password_change(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        change_password(
            request.user,
            serializer.validated_data["old_password"],
            serializer.validated_data["new_password"],
        )
        return Response(status=status.HTTP_200_OK)

    @action(
        methods=["GET"],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def get_user_info(self, request):
        data = serializers.AuthUserSerializer(request.user).data
        return Response(data=data, status=status.HTTP_200_OK)

    @action(
        methods=["POST"],
        detail=False,
        permission_classes=[
            IsAuthenticated,
        ],
    )
    def update_user_info(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = update_user_info(request.user, **serializer.data)
        login(request, user)
        return Response(status=status.HTTP_200_OK)


class ListUsersViewSet(generics.ListAPIView):
    serializer_class = serializers.UserSerializer
    queryset = Person.objects.all()
    permission_classes = [
        AllowAny,
    ]


class GetUserView(viewsets.ModelViewSet):
    serializer_class = serializers.FullUserSerializer

    def get_queryset(self):
        return Person.objects.filter(id=self.kwargs["id"])

