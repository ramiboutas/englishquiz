# from django.contrib.auth import get_user_model
# from django.test import TestCase
# from blog.models import BlogPost
# from blog import tasks
# from celery.contrib.testing.worker import start_worker
# from django.test import TransactionTestCase
# User = get_user_model()
# from config.celery import app
# class BlogTaskTests(TransactionTestCase):
#     """
#     Testing the BlogPost model.
#     """
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.celery_worker = start_worker(app, log="info", perform_ping_check=False, concurrency=2)
#         cls.celery_worker.__enter__()
#     @classmethod
#     def tearDownClass(cls):
#         super().tearDownClass()
#         cls.celery_worker.__exit__(None, None, None)
#     def setUp(self):
#         self.user = User.objects.create_user(
#             username="test-user", password="test-password"
#         )
#         content = """
#         Lorem Ipsum is simply dummy text of the printing and typesetting industry.
#         Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
#         when an unknown printer took a galley of type and scrambled it to make a type specimen book.
#         It has survived not only five centuries, but also the leap into electronic typesetting,
#         remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset
#         sheets containing Lorem Ipsum passages, and more recently with desktop publishing software
#          like Aldus PageMaker including versions of Lorem Ipsum.
#         """
#         self.post = BlogPost.objects.create(
#             title="Test title",
#             description="This is my description",
#             created_by=self.user,
#             public=True,
#             content=content,
#         )
#         self.task = tasks.create_blog_post_pdf.apply_async(countdown=1, kwargs={"pk": self.post.pk})
#     def test_pdf_created(self):
#         self.assertTrue(self.post.pdf)
