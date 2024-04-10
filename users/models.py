
# 1)版本1：是最后两个自定义类，同时setting定义了author引用管道
# 2)版本2：增加一个用户管理器，前面两个类，并将之前的user类的自定义字段，扩展自AbstractBaseUser和PermissionsMixin的用户模型
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):              # PermissionsMixin include is_active,is_staff etc..
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)

    # add user other fields if necessary
    is_active = models.BooleanField(default=True)            # Whether the user account is activated for login
    is_staff = models.BooleanField(default=False)            # Whether users can log in to Django's administration backend
    date_joined = models.DateTimeField(default=timezone.now) # Time of user registration
    preferList = models.JSONField(default=dict)              # User Preference List
    is_first_login = models.BooleanField(default=True)
    profile_pic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)   #  User's personal photo
    birth_date = models.DateField(null=True, blank=True)     # User's birthday
    bio = models.TextField(blank=True)                       # User profiles

    objects = UserManager()

    USERNAME_FIELD = 'email'                                 # Set the login field
    REQUIRED_FIELDS = ['username']                           # import! Required when creating a superuser, aside from email and password

    # def set_password(self, raw_password):
    #     self.password = make_password(raw_password)
    #     self._password = raw_password

    def set_prefer_list(self, prefer_list):
        self.is_first_login = False
        self.preferList = prefer_list
        self.save()

    def __str__(self):
        return self.username


class NewsLog(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)           # user - news
    news_id = models.CharField(max_length=255)
    body = models.TextField()
    keywords = models.TextField()
    timestamp = models.DateTimeField()
    title = models.CharField(max_length=255)