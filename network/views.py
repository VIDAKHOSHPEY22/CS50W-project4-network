from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow, Comment


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/index.html", {
        "page_obj": page_obj
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@login_required
def new_post(request):
    if request.method == "POST":
        content = request.POST.get("content")
        image = request.POST.get("image")  # Get the image URL
        if content:
            Post.objects.create(author=request.user, content=content, image=image)
        return redirect("index")
    return redirect("index")


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=profile_user).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Followers and following counts
    followers_count = profile_user.followers.count() if hasattr(profile_user, 'followers') else 0
    following_count = profile_user.following.count() if hasattr(profile_user, 'following') else 0

    # Is the current user following this profile?
    is_following = False
    if request.user.is_authenticated and request.user != profile_user:
        is_following = profile_user.followers.filter(user=request.user).exists()

    followers = profile_user.followers.all()
    following = profile_user.following.all()

    return render(request, "network/profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "followers_count": followers_count,
        "following_count": following_count,
        "is_following": is_following,
        "followers": followers,
        "following": following,
    })


@login_required
def following(request):
    # Get users that the current user follows
    following_users = request.user.following.values_list('following', flat=True)
    # Get posts from those users
    posts = Post.objects.filter(author__in=following_users).order_by('-timestamp')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "network/following.html", {
        "page_obj": page_obj
    })


@require_POST
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user
    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return JsonResponse({"likes": post.likes.count(), "liked": liked})


@csrf_exempt
@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            post.content = content
            post.save()
    return redirect(request.META.get("HTTP_REFERER", "index"))


@login_required
@require_POST
def follow_user(request, username):
    target = get_object_or_404(User, username=username)
    if target != request.user:
        Follow.objects.get_or_create(user=request.user, following=target)
    return redirect("profile", username=username)

@login_required
@require_POST
def unfollow_user(request, username):
    target = get_object_or_404(User, username=username)
    if target != request.user:
        Follow.objects.filter(user=request.user, following=target).delete()
    return redirect("profile", username=username)

@login_required
def edit_profile(request):
    if request.method == "POST":
        profile_image = request.POST.get("profile_image")
        request.user.profile_image = profile_image
        request.user.save()
    return redirect("profile", username=request.user.username)

@login_required
def add_comment(request, post_id):
    if request.method == "POST":
        content = request.POST.get("content")
        parent_id = request.POST.get("parent_id")
        post = get_object_or_404(Post, id=post_id)
        parent = None
        if parent_id:
            try:
                parent = Comment.objects.get(id=parent_id)
            except Comment.DoesNotExist:
                parent = None
        if content:
            Comment.objects.create(
                author=request.user,
                post=post,
                content=content,
                parent=parent
            )
    return redirect(request.META.get("HTTP_REFERER", "index"))

