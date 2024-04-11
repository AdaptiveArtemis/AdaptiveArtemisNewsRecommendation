from django.db import models

# Define the data model for crawling
from django.db import models
# from django.utils import timezone             # Ireland Time

class Article(models.Model):
    title = models.CharField(max_length=255)
    link = models.URLField()
    description = models.TextField()
    pub_date = models.DateTimeField()
    image = models.URLField()
    author = models.CharField(max_length=255, null=True, blank=True)
    category = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.TextField(null=True, blank=True)
    robots = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    # timestamp = models.DateTimeField(auto_now_add=True,default=timezone.now)
    timestamp = models.DateTimeField(auto_now_add=True)
    keywords1 = models.JSONField(default=list)

    def __str__(self):
        return self.title