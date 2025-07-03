from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        error_messages={
            "required": "Email is required.",
            "invalid": "Enter a valid email address."
        }
    )
    password = serializers.CharField(
        required=True,
        min_length=6,
        error_messages={
            "required": "Password is required.",
            "min_length": "Password must be at least 6 characters long."
        }
    )
