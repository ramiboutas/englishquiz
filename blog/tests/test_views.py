from django.test import TestCase
from django.urls import reverse

from blog.models import BlogPost


class BlogViewTests(TestCase):
    """
    Testing the BlogPost model.
    """

    def setUp(self):

        posts = []
        for count in range(10):
            posts.append(
                BlogPost(
                    title=f"Test title {count}",
                    description="This is my description",
                    public=True,
                    content=f"This is my content for post {count}",
                )
            )
        self.posts = BlogPost.objects.bulk_create(posts)
        self.post = self.posts[0]

    def test_post_list_view(self):
        url = reverse("blog_postlist")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_list.html")

    def test_all_posts_view(self):
        url = reverse("blog_allposts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/all_posts.html")

    def test_post_detail_view(self):
        url = self.post.get_absolute_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_detail.html")
