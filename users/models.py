from django.db import models

# Create your models here.

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    preferList = models.JSONField(default=list) # 用户偏好列表的JSON字符串
    is_first_login = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def set_prefer_list(self, prefer_list):
        self.is_first_login = False
        self.preferList = prefer_list
        self.save()

    def __str__(self):
        return self.username

class NewsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    news_id = models.CharField(max_length=255)
    content = models.TextField()  # 新闻内容
    keywords = models.TextField()  # 新闻关键词列表的JSON字符串
    timestamp = models.DateTimeField()
    title = models.CharField(max_length=255)