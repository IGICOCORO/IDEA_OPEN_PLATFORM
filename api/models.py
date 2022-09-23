from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Tags(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tags")

class Posts(models.Model):
    name = models.CharField(max_length=50)
    content = models.TextField(max_length=1000)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField('Tags', related_name='posts')
    is_liked = models.BooleanField()

    def __str__():
    	return f"{self.content} {self.tags}"

class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    comment = models.TextField(max_length=400)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.comment[:60]
