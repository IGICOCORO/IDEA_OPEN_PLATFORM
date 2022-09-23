from django.db import models
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Tags(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=50, unique=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_tags")

    def __str__(self):
        return f"{self.name} {self.created_by}"

class Posts(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    content = models.TextField(max_length=1000)
    is_liked = models.BooleanField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    tags = models.ManyToManyField('Tags', related_name='posts')

    def __str__(self):
        return f"{self.name} {self.content} {self.created_by}"

class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    comment = models.TextField(max_length=400)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return self.comment[:60]
