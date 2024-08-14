from django.db.models import Manager, QuerySet
from django.utils.timezone import now


class CustomQuerySet(QuerySet):
    def filtered_posts(self):
        return self.filter(
            is_published=True,
            pub_date__lte=now(),
            category__is_published=True
        ).select_related(
            'author',
            'category',
            'location',
        )


class FilteredManager(Manager):
    def get_queryset(self):
        return CustomQuerySet(self.model, using=self._db)

    def filtered_posts(self):
        return self.get_queryset().filtered_posts()