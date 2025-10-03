from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime 
from django.utils import timezone

now =  datetime.now()
time = now.strftime("%d %B %Y")

class CustomUserModel(AbstractUser):
    bio=models.TextField(null=True,blank=True)
    linked_in=models.URLField(max_length=255,null=True,blank=True)
    instagram=models.URLField(max_length=255,null=True,blank=True)
    profile_picture=models.ImageField(upload_to='profile_img',blank=True,null=True)

    def __str__(self):
        return self.username


# Models for Blogs

class Category(models.Model):
    name=models.CharField(max_length=255,null=False,blank=False)
    description=models.CharField(max_length=255,null=True,blank=True)

    def __str__(self):
        return self.name

class Blogs(models.Model):
    title=models.CharField(max_length=255,null=False,blank=False)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='blogs')
    image=models.ImageField(upload_to='blog_img',null=True,blank=True)
    description=models.TextField()
    time = models.DateTimeField(default=timezone.now, blank=True)
    likes=models.ManyToManyField(CustomUserModel,related_name='liked_blogs',blank=True)
    user=models.ForeignKey(CustomUserModel,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} uploaded {self.title}"
    
    @property
    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    content = models.CharField(max_length=200)
    time = models.DateTimeField(default=timezone.now, blank=True)
    blogs = models.ForeignKey(Blogs, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} commented {self.content} on {self.blogs.title}"


class Contact(models.Model):
    name=models.CharField(max_length=255)
    email=models.EmailField(max_length=255)
    subject=models.CharField(max_length=255)
    message=models.CharField(max_length=255,blank=True)

