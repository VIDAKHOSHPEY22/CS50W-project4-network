from django.contrib import admin
from .models import User, Post, Comment, Follow

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "date_joined")
    search_fields = ("username", "email")

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "content", "timestamp")
    search_fields = ("author__username", "content")
    list_filter = ("timestamp",)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "post", "content", "timestamp", "parent")
    search_fields = ("author__username", "content")
    list_filter = ("timestamp",)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ("user", "following")
    search_fields = ("user__username", "following__username")
