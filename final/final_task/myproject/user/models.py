from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django import forms

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, first_name, last_name, role=None):
        user = User(email=email, password=password, first_name=first_name, last_name=last_name)
        if role is not None:
            user.role = role
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name):

        user = self.create_user(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    email = models.EmailField(unique=True, db_index=True)
    username = models.CharField(max_length=25, blank=True, null=True)
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    TEACHER = 'teacher'
    STUDENT = 'student'

    USER_ROLES_CHOICES = (
        (TEACHER, 'teacher'),
        (STUDENT, 'student'),
    )
    role = models.CharField(max_length=255,
                            choices=USER_ROLES_CHOICES,
                            default=STUDENT,
                            blank=True,
                            null=True)

    #courses = models.ManyToManyField(Course, related_name='user')

    REQUIRED_FIELDS = ['password', 'first_name', 'last_name']

    def get_full_name(self):
        full_name = self.first_name + self.last_name
        return full_name

    def __str__(self):
        return self.email


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'role')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user