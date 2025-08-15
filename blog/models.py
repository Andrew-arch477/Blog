from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Avg

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('writer', 'Writer'),
        ('user', 'User'),
    ]

    role = models.CharField(max_length=6, choices=ROLE_CHOICES, default='user')

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Tag(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Article(models.Model):
    STAGE_CHOICES = [
        ('done', 'Done'),
        ('skatch', 'Skatch'),
    ]

    name = models.CharField(max_length=30)
    text = models.TextField()
    category = models.ManyToManyField(Category, related_name='article', blank=True)
    tags = models.ManyToManyField(Tag, related_name='article', blank=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    stage = models.CharField(max_length=6, choices=STAGE_CHOICES, default='skatch')

    def rating_average(self):
        return self.ratings.aggregate(avg=Avg('rate'))['avg'] or 0
    
    def __str__(self):
        return self.name

class Rating(models.Model):
    rate = models.IntegerField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.article}"

class Announcement(models.Model):
    name = models.CharField(max_length=30)
    text = models.TextField()

    def __str__(self):
        return self.name
