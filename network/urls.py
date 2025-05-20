from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_post", views.new_post, name="new_post"),
    path("profile/<str:username>", views.profile, name="profile"),
    path("following", views.following, name="following"),
    path("like/<int:post_id>", views.like_post, name="like_post"),
    path("edit_post/<int:post_id>", views.edit_post, name="edit_post"),
    path("follow/<str:username>", views.follow_user, name="follow_user"),
    path("unfollow/<str:username>", views.unfollow_user, name="unfollow_user"),
    path("edit_profile", views.edit_profile, name="edit_profile"),
    path("comment/<int:post_id>", views.add_comment, name="add_comment"),
]
