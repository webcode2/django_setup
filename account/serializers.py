import warnings
from abc import ABC

from pydantic import ValidationError
from rest_framework import serializers
from django.http.response import HttpResponseBadRequest
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.template.loader import get_template

from account.models import User
from django.utils import timezone

from core.utils.helper_fuctions import verify_email
from core.utils.schamas import UserCreateSchema
from core.utils.sendEmail import send_email
from core.settings import SEND_EMAIL_FROM


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        print(user)

        # Add custom claims
        token["email"] = user.email
        token["role"] = user.is_superuser
        token['last_name'] = user.last_name
        token['first_name'] = user.first_name

        return token


#  password reset


# users 
class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name","last_name",'email', 'password']
        # fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}

    #


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", 'is_active', 'is_staff', "is_superuser", "last_login",
                  "date_joined"]
        extra_kwargs = {
            'password': {'write_only': True},
            'is_active': {'read_only': True},
            'is_staff': {'read_only': True},
            "is_superuser": {'read_only': True},
            "last_login": {'read_only': True},
            "date_joined": {'read_only': True},

        }

    def create(self, validated_data):

        try:
            UserCreateSchema(**validated_data)
            user: User = User(
                email=validated_data['email'],
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                is_active=True,
                last_login=timezone.now()
            )
            user.set_password(validated_data['password'])
            user.save()
            try:
                html_email = get_template("email_template/p_reset_success.html").render(context={"user": user})
                send_email(email_from=SEND_EMAIL_FROM, html_email=html_email,
                           to_email=user.email, subject="account Creation Successful")
            except:
                warnings.warn("Email not configured")
                pass

            return user

        except ValidationError as e:
            raise serializers.ValidationError({"message": e.errors()})


class AccountRecoverySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', "last_login"]


class PasswordRecoverySerializer(serializers.Serializer, ):
    email = serializers.EmailField()
