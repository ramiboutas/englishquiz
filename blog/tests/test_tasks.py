from blog.tasks import create_blog_post_pdf


from django.test import TestCase
from blog.models import BlogPost


def TaskTests(TestCase):
    """
    Testing the BlogPost model.
    """
    def setUp(self):
        content = """
        Lorem Ipsum is simply dummy text of the printing and typesetting industry.
        Lorem Ipsum has been the industry's standard dummy text ever since the 1500s,
        when an unknown printer took a galley of type and scrambled it to make a type specimen book.
        It has survived not only five centuries, but also the leap into electronic typesetting,
        remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset
        sheets containing Lorem Ipsum passages, and more recently with desktop publishing software
         like Aldus PageMaker including versions of Lorem Ipsum.
        """
        self.post_pdf = BlogPost.objects.create(
            title="Test title",
            description="This is my description",
            public=True,
            content=content,
        )
    
    def test_pdf_creation(self):
        create_blog_post_pdf(kwargs={"pk": self.post_pdf.pk})
        self.assertTrue(self.post_pdf.pdf)





