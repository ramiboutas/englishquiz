from celery import shared_task

from affiliates.models import Book


@shared_task(bind=True)
def update_featured_books(self, **kwargs):
    qs = Book.objects.all()
    qs.update(featured=False)
    new_featured = qs[:6]
    Book.objects.filter(id__in=new_featured).update(featured=True)
