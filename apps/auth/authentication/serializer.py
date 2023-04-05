from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from apps.account.models import User
from apps.auth.jwt.v1.tasks import send_mail_reset_password
from apps.common.custom_exception_handler import CustomAPIException


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=64, required=True)
    password = serializers.CharField(max_length=64, required=True, help_text='Leave empty if no change needed',
                                     style={'input_type': 'password'})

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if not username or not password:
            raise serializers.ValidationError('password and username field required')

        if user := authenticate(username=username, password=password):
            return user
        else:
            raise AuthenticationFailed()


class PasswordChangeSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=32, required=True)
    new_password = serializers.CharField(max_length=32, required=True)
    verified_password = serializers.CharField(max_length=32, required=True)

    def validate(self, data):
        password = data.get('password', None)
        new_password = data.get('new_password', None)
        verified_password = data.get('verified_password', None)

        user = self.context.get('request').user
        if not user.check_password(password):
            raise CustomAPIException('Your current password is incorrect.')

        if new_password != verified_password:
            raise CustomAPIException('Your passwords didnt match.')

        return data

    def create(self, validated_data):
        new_password = validated_data.get('new_password', None)

        user = self.context.get('request').user
        user.set_password(new_password)
        user.save()
        return validated_data


class PasswordResetSerializer(serializers.Serializer):
    username = serializers.EmailField(max_length=32, required=True)

    def validate(self, data):
        username = data.get('username', None)
        user = User.objects.filter(email=username).first()
        if not user:
            raise serializers.ValidationError('username is not exists')
        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data.get('user')
        new_password = user.make_random_password()
        user.set_password(new_password)
        user.save()

        send_mail_reset_password.delay(user.email, new_password)

        return validated_data
