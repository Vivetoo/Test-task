from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import CustomUser, Teacher

class CustomUserSerializer(ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'second_name','last_name', 'email')

class TeacherSerializer(ModelSerializer):

    class Meta:
        model = Teacher


class StudentRegSerializer(ModelSerializer):
    first_name = serializers.CharField(required=True)
    second_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)
    is_student = serializers.BooleanField(default=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True,)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'second_name', 'last_name', 'email', 'is_student', 'password','password2')
        extra_kwargs = {'password': {'write_only': True}}

    def save(self):
        user = CustomUser(
            email=self.validated_data['email'],
            first_name=self.validated_data['first_name'],
            second_name=self.validated_data['second_name'],
            last_name=self.validated_data['last_name'],
            is_student=self.validated_data['is_student'],
        )
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords do not match'})
        user.set_password(password)
        user.save()
        return user


class StudentLogSerializer(ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}




