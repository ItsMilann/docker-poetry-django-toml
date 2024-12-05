# pylint:disable=c0115
from uuid import uuid4

from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from users import constants, models


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = [
            "id",
            "email",
            "password",
            "role",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = models.User.objects.create(**validated_data)
        password = validated_data.get("password", uuid4().hex)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        password = validated_data.get("password")
        if password:
            user.set_password(password)
            user.save()
        return instance


class BaseProfile(serializers.ModelSerializer):
    """
    Serializer for BaseProfile model.

    This serializer is used for creating and updating BaseProfile instances.
    It handles the creation and updating of associated User instances.
    """

    def __create_user(self, data):
        """
        Creates a new User instance based on the provided data.
        """
        serializer = UserSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def __update_user(self, instance, data):
        """
        Updates the provided User instance with the provided data.
        """
        serializer = UserSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    @transaction.atomic
    def create(self, validated_data):
        """
        Creates a new BaseProfile instance with the provided validated data.
        Creates a new User instance with the provided data and associates it with the BaseProfile.
        """
        request = self.context["request"]
        user = self.__create_user(request.data)
        validated_data["user"] = user
        return self.Meta.model.objects.create(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Updates the provided BaseProfile instance with the provided validated data.
        Updates the associated User instance with the provided data.
        """
        request = self.context["request"]
        self.__update_user(instance.user, request.data)
        return super().update(instance, validated_data)


class TokenSerializer(TokenObtainPairSerializer):
    """
    TokenSerializer for generating refresh and access tokens.
    Adds phone and role fields to the response.
    """

    def validate(self, attrs):
        """
        Validates the token and returns a dictionary with refresh and access tokens
        along with the user's phone and role.
        """
        data = super().validate(attrs)
        refresh = self.get_token(self.user)
        # assert isinstance(self.user, models.User)
        data["role"] = self.user.role
        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data


class ProfileSerializer(BaseProfile):
    """
    Serializer for Profile model. Read only fields are user's email and role.
    User field is optional.
    """

    role = serializers.ReadOnlyField(source="user.role")
    user = UserSerializer(required=False)

    class Meta:
        model = models.Profile
        fields = "__all__"


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Document
        fields = "__all__"


class PaymentInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.PaymentInfo
        fields = "__all__"


class ProfileDetailSerializer(BaseProfile):
    """
    Serializer for Profile model. Read only fields are user's email and role.
    User field is optional.
    """

    role = serializers.ReadOnlyField(source="user.role")
    user = UserSerializer(required=False)
    paymentInfo = serializers.SerializerMethodField()
    documents = serializers.SerializerMethodField()

    class Meta:
        model = models.Profile
        fields = "__all__"

    def get_paymentInfo(self, obj):
        return PaymentInfoSerializer(obj.paymentInfo.all(), many=True).data

    def get_documents(self, obj):
        return DocumentSerializer(obj.documents.all(), many=True).data
