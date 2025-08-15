from django.contrib import admin
from .models import Article, Comment, User, Announcement, Category, Tag, Rating

admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(User)
admin.site.register(Announcement)
admin.site.register(Category)
admin.site.register(Rating)
admin.site.register(Tag)
