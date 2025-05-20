from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from .models import Post, Comment, Follow

User = get_user_model()

class NetworkTestCase(TestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(username="user1", password="pass1234")
        self.user2 = User.objects.create_user(username="user2", password="pass1234")
        # Create posts
        self.post1 = Post.objects.create(author=self.user1, content="Hello World!", image="https://example.com/img1.jpg")
        self.post2 = Post.objects.create(author=self.user2, content="Second post")
        # Create follow
        Follow.objects.create(user=self.user1, following=self.user2)
        # Create comment
        self.comment = Comment.objects.create(post=self.post1, author=self.user2, content="Nice post!")

    def test_post_creation(self):
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(self.post1.author.username, "user1")
        self.assertEqual(self.post1.content, "Hello World!")

    def test_following(self):
        self.assertEqual(self.user1.following.count(), 1)
        self.assertEqual(self.user2.followers.count(), 1)

    def test_comment(self):
        self.assertEqual(self.post1.comments.count(), 1)
        self.assertEqual(self.comment.content, "Nice post!")

    def test_profile_page(self):
        c = Client()
        response = c.get(f"/profile/{self.user1.username}")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.user1.username)

    def test_add_comment_view(self):
        c = Client()
        c.login(username="user1", password="pass1234")
        response = c.post(f"/comment/{self.post2.id}", {"content": "Test comment"})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.post2, content="Test comment").exists())

    def test_edit_post(self):
        c = Client()
        c.login(username="user1", password="pass1234")
        response = c.post(f"/edit_post/{self.post1.id}", {"content": "Edited!"})
        self.assertEqual(response.status_code, 302)
        self.post1.refresh_from_db()
        self.assertEqual(self.post1.content, "Edited!")

    def test_like_post(self):
        c = Client()
        c.login(username="user1", password="pass1234")
        response = c.post(f"/like/{self.post2.id}")
        self.assertIn(self.user1, self.post2.likes.all())
