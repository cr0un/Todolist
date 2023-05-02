from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from core.models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_repeat = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password_repeat', 'email', 'first_name', 'last_name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password_repeat']:
            raise serializers.ValidationError({"password_repeat": "Пароли не совпадают."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email')
        read_only_fields = ('id',)


class PasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

