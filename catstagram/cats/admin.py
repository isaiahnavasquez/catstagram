from django.contrib import admin

from .models import Comment, Post, Profile, Relationship, Hashtag, Like

admin.site.register(Comment)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Relationship)
admin.site.register(Hashtag)
admin.site.register(Like)
