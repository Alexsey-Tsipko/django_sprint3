from django.db.models import QuerySet
from django.utils.timezone import now


class CustomQuerySet(QuerySet):
    def get_queryset(self):
        return super().get_queryset().filter(
            is_published=True,
            pub_date__lte=now(),
            category__is_published=True
        ).select_related(
            'author',
            'category',
            'location',
        )
