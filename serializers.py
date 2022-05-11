from rest_framework import serializers

from user.models import Person


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("id", "username", "email", "password")


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(required=True, write_only=True)


class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ("username", "email", "first_name", "last_name", "about", "image")

    @classmethod
    def get_token(cls, user):
        token = super(AuthUserSerializer, cls).get_token(user)

        # Add custom claims
        token["username"] = user.username
        return token


class EmptySerializer(serializers.Serializer):
    pass


class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["id", "username", "tg_username"]


class FullUserSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name="profile", lookup_field="username")

    class Meta:
        model = Person
        fields = ["id", "username", "url", "email", "first_name", "second_name", "coins", "tg_username"]
