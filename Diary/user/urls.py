from django.urls import path

from .views import StudentRegisterAPIView, StudentLoginAPIView, ProfileAPIView

urlpatterns = [
    path('/register/', StudentRegisterAPIView.as_view({'post': 'post'}), name='register'),
    path('/login/', StudentLoginAPIView.as_view({'post': 'post'}), name='login'),
    path('/profile/', ProfileAPIView.as_view({'get': 'get'}), name='profile'),
]