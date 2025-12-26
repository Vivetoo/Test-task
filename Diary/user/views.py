from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response

from user.serializer import StudentRegSerializer, StudentLogSerializer, CustomUserSerializer
from .models import CustomUser
from .permission import IsAnonymous
from .token import get_token


class StudentRegisterAPIView(ViewSet):
    permission_classes = [IsAnonymous]
    serializer_class = StudentRegSerializer

    def post(self, request):
        serializer = StudentRegSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(StudentRegSerializer(user).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StudentLoginAPIView(ViewSet):
    permission_classes = [IsAnonymous]
    serializer_class = StudentLogSerializer

    def post(self, request):

        serializer = StudentLogSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            try:
                user = authenticate(email=serializer.validated_data['email'],
                                    password=serializer.validated_data['password'])
            except CustomUser.DoesNotExist:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            if user:
                token = get_token(user)
                return Response({'message': 'Login successfull',
                                      'token': token}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class ProfileAPIView(ViewSet):
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        user = CustomUser.objects.get(id=request.user.id)
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
