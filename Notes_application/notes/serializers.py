from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import CustomUser, Note, Image, NoteShare
from rest_framework.validators import UniqueValidator

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    mobile_number = serializers.CharField(max_length=10, validators=[RegexValidator(
        regex=r'^\d{10}$',
        message='Mobile number must be a 10-digit number.',
    ),
    UniqueValidator(
        queryset=CustomUser.objects.all(),
        message='This mobile number is already in use.',
    )])
    email = serializers.EmailField(validators=[
        RegexValidator(
            regex=r'@(example\.com|demo\.com)$',
            inverse_match=True,
            message='Email address cannot have @example.com or @demo.com domain.',
        )
    ])

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'password', 'mobile_number')

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 12 characters long.")
        if not any(char.isupper() for char in value):
            raise serializers.ValidationError("Password must contain at least one capital letter.")
        if not any(char.isdigit() for char in value):
            raise serializers.ValidationError("Password must contain at least one number.")
        # if value in self.instance.username or value in self.instance.email:
        #     raise serializers.ValidationError("Password cannot contain the username or email.")
        return value

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ('id', 'note', 'image')

    def validate_image(self, value):
        if value.size > 2 * 1024 * 1024:  # 2MB limit
            raise serializers.ValidationError("Image size cannot exceed 2MB.")
        if not value.name.endswith('.png'):
            raise serializers.ValidationError("Only PNG images are allowed.")
        return value

class NoteSerializer(serializers.ModelSerializer):
    owner = CustomUserSerializer()
    # owner = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all()) 

    images = ImageSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'owner', 'title', 'content', 'created_at', 'updated_at', 'images')

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("Content cannot be blank.")
        return value

class NoteShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = NoteShare
        fields = ('id', 'note', 'user')