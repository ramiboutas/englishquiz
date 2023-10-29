from huey import crontab
from huey.contrib import djhuey as huey

from affiliates.models import Book


@huey.db_periodic_task(crontab(hour="00", minute="30"))
def update_featured_books():
    qs = Book.objects.all()
    qs.update(featured=False)
    new_featured = qs[:6]
    Book.objects.filter(id__in=new_featured).update(featured=True)
