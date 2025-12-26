from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser


class CustomUserManager(BaseUserManager):

    def create_user(self, email, first_name, second_name, last_name, password, **extra_fields):
        if not email:
            raise ValueError('User must have an email')

        user = self.model(email=self.normalize_email(email),
                          first_name=first_name,
                          second_name=second_name,
                          last_name=last_name,
                          **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, first_name, second_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('is_stuff must be True!')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('is_superuser must be True!')

        return self.create_user(email, first_name, second_name, last_name, password, **extra_fields)


class CustomUser(AbstractUser):

    email = models.EmailField(max_length=100, unique=True, verbose_name='Почта')
    first_name = models.CharField(max_length=55, verbose_name='Имя')
    second_name = models.CharField(max_length=55, verbose_name='Фамилия')
    last_name = models.CharField(max_length=55, verbose_name='Отчество')

    is_director = models.BooleanField(default=False, verbose_name='Директор')
    is_teacher = models.BooleanField(default=False, verbose_name='Учитель')
    is_student = models.BooleanField(default=False, verbose_name='Студент')


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('first_name', 'second_name', 'last_name')
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Teacher(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Учитель'
        verbose_name_plural = 'Учителя'


    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Студент'
        verbose_name_plural = 'Студенты'

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'
