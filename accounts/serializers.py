from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import User

class SignUpSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=250)
    email = serializers.CharField(max_length=100)
    password = serializers.CharField(min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["name", "email", "password"]

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs["email"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")

        return super().validate(attrs)

    def create(self, validated_data):
        password = validated_data.pop("password")

        user = super().create(validated_data)

        user.set_password(password)

        user.save()

        return user